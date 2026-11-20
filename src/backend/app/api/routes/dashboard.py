from collections import Counter, defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.ml.preprocessing import reason_to_group
from app.models.absence_record import AbsenceRecord
from app.models.employee import Employee
from app.models.model_version import ModelVersion
from app.models.prediction import Prediction
from app.schemas.dashboard import DashboardStats, ModelInfo, MonthlyAverage, ReasonGroupBreakdown

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    dependencies=[Depends(get_current_user)]
)


@router.get("/stats", response_model=DashboardStats)
def get_stats(db: Session = Depends(get_db)):
    """Aggregate figures for the dashboard: totals, excessive rate, breakdowns, active model."""
    total_employees = db.query(func.count(Employee.id)).scalar() or 0
    total_predictions = db.query(func.count(Prediction.id)).scalar() or 0
    total_absence_records = db.query(func.count(AbsenceRecord.id)).scalar() or 0
    excessive_count = db.query(func.count(Prediction.id)).filter(Prediction.is_excessive.is_(True)).scalar() or 0
    excessive_rate = (excessive_count / total_predictions) if total_predictions else 0.0

    reason_codes = [r[0] for r in db.query(AbsenceRecord.reason_for_absence).all()]
    group_counts = Counter(reason_to_group(code) for code in reason_codes)
    reason_breakdown = [
        ReasonGroupBreakdown(reason_group=group, count=count)
        for group, count in sorted(group_counts.items())
    ]

    date_hours = db.query(AbsenceRecord.absence_date, AbsenceRecord.absenteeism_time_in_hours).all()
    month_hours: dict[int, list[int]] = defaultdict(list)
    for absence_date, hours in date_hours:
        month_hours[absence_date.month].append(hours)
    monthly_average_hours = [
        MonthlyAverage(month=month, average_hours=sum(hours_list) / len(hours_list))
        for month, hours_list in sorted(month_hours.items())
    ]

    active_version = db.query(ModelVersion).filter(ModelVersion.is_active.is_(True)).first()
    active_model = (
        ModelInfo(
            version=active_version.version,
            accuracy=active_version.accuracy,
            precision=active_version.precision,
            recall=active_version.recall,
            f1_score=active_version.f1_score,
            roc_auc=active_version.roc_auc,
            trained_at=active_version.trained_at.isoformat(),
        )
        if active_version
        else None
    )

    return DashboardStats(
        total_employees=total_employees,
        total_predictions=total_predictions,
        total_absence_records=total_absence_records,
        excessive_rate=excessive_rate,
        reason_breakdown=reason_breakdown,
        monthly_average_hours=monthly_average_hours,
        active_model=active_model,
    )
