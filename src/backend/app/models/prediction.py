from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Prediction(Base):
    """An archived prediction, kept for traceability and dashboard stats.

    Records what was predicted, for whom, by whom, and with which model version.
    ``employee_id`` and ``requested_by_id`` are optional and set to NULL rather
    than deleted if their employee/user is removed, so history is preserved.
    ``input_features`` freezes the exact feature values used.
    """

    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )
    requested_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    reason_for_absence: Mapped[int] = mapped_column(Integer, nullable=False)
    absence_date: Mapped[date] = mapped_column(Date, nullable=False)
    input_features: Mapped[dict] = mapped_column(JSON, nullable=False)
    probability: Mapped[float] = mapped_column(Float, nullable=False)
    is_excessive: Mapped[bool] = mapped_column(Boolean, nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    employee = relationship("Employee", back_populates="predictions")
