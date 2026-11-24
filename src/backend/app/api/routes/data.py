from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.config import get_settings
from app.database import get_db
from app.ml.dataset import build_training_dataframe
from app.ml.importer import import_raw_csv
from app.ml.train import train_and_evaluate
from app.models.model_version import ModelVersion
from app.schemas.dashboard import ModelInfo

router = APIRouter(prefix="/data", tags=["data & model"], dependencies=[Depends(get_current_user)])
settings = get_settings()


@router.post("/import-csv", status_code=status.HTTP_201_CREATED)
def import_csv(file: UploadFile, db: Session = Depends(get_db)):
    """Import a raw absenteeism CSV into employees + absence_records."""
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please upload a .csv file")
    content = file.file.read()
    try:
        imported = import_raw_csv(db, content)
    except (KeyError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Could not parse CSV: {exc}",
        ) from exc
    return {"imported_records": imported}


@router.post("/train", response_model=ModelInfo)
def train_model(db: Session = Depends(get_db)):
    """Train a new model on all stored data, activate it, and return its metrics."""
    df = build_training_dataframe(db)
    try:
        result = train_and_evaluate(df, settings.ml_artifacts_dir)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    db.query(ModelVersion).update({ModelVersion.is_active: False})
    version = ModelVersion(
        version=result.version,
        is_active=True,
        n_train_samples=result.n_train_samples,
        n_test_samples=result.n_test_samples,
        accuracy=result.accuracy,
        precision=result.precision,
        recall=result.recall,
        f1_score=result.f1_score,
        roc_auc=result.roc_auc,
        artifact_path=str(result.artifact_dir),
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    return ModelInfo(
        version=version.version,
        accuracy=version.accuracy,
        precision=version.precision,
        recall=version.recall,
        f1_score=version.f1_score,
        roc_auc=version.roc_auc,
        trained_at=version.trained_at.isoformat(),
    )


@router.get("/model-versions", response_model=list[ModelInfo])
def list_model_versions(db: Session = Depends(get_db)):
    """List every trained model version, most recent first."""
    versions = db.query(ModelVersion).order_by(ModelVersion.trained_at.desc()).all()
    return [
        ModelInfo(
            version=v.version,
            accuracy=v.accuracy,
            precision=v.precision,
            recall=v.recall,
            f1_score=v.f1_score,
            roc_auc=v.roc_auc,
            trained_at=v.trained_at.isoformat(),
        )
        for v in versions
    ]
