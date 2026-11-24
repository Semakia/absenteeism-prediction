from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.ml.predict import load_model_bundle, predict_one
from app.models.employee import Employee
from app.models.model_version import ModelVersion
from app.models.prediction import Prediction
from app.models.user import User
from app.schemas.prediction import PredictionOut, PredictionRequest, PredictionResult

router = APIRouter(prefix="/predictions", tags=["predictions"], dependencies=[Depends(get_current_user)])


def _get_active_model_version(db: Session) -> ModelVersion:
    version = db.query(ModelVersion).filter(ModelVersion.is_active.is_(True)).first()
    if version is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No trained model is available yet. Trigger POST /data/train first.",
        )
    return version


@router.post("/predict", response_model=PredictionResult)
def predict(
    payload: PredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Score one absence event (for a stored employee or ad-hoc features) and archive it."""
    model_version = _get_active_model_version(db)
    bundle = load_model_bundle(model_version.artifact_path)

    employee: Employee | None = None
    if payload.employee_id is not None:
        employee = db.get(Employee, payload.employee_id)
        if employee is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        features = {
            "transportation_expense": employee.transportation_expense,
            "distance_to_work": employee.distance_to_work,
            "age": employee.age,
            "daily_work_load_average": employee.daily_work_load_average,
            "body_mass_index": employee.body_mass_index,
            "education": employee.education,
            "children": employee.children,
            "pets": employee.pets,
        }
    else:
        features = payload.manual_features.model_dump()

    probability, is_excessive = predict_one(
        bundle,
        reason_for_absence=payload.reason_for_absence,
        absence_date=payload.absence_date,
        **features,
    )
    record = Prediction(
        employee_id=employee.id if employee else None,
        requested_by_id=current_user.id,
        reason_for_absence=payload.reason_for_absence,
        absence_date=payload.absence_date,
        input_features=features,
        probability=probability,
        is_excessive=is_excessive,
        model_version=bundle.version,
    )
    db.add(record)
    db.commit()
    return PredictionResult(probability=probability, is_excessive=is_excessive, model_version=bundle.version)


@router.get("", response_model=list[PredictionOut])
def list_predictions(
    db: Session = Depends(get_db),
    employee_id: int | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    """List archived predictions, optionally filtered by employee, most recent first."""
    query = db.query(Prediction)
    if employee_id is not None:
        query = query.filter(Prediction.employee_id == employee_id)
    return query.order_by(Prediction.created_at.desc()).offset(offset).limit(limit).all()
