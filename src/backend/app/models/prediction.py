from datetime import date, datetime, timezone

from sqlachemy import (
    Boolean, Date, DateTime, Float, ForeignKey, Integer, JSON, String
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Prediction(Base):
    """"
    An employee whose demographic and work data feed the ML model.

    Each column (transportation_expense, distance_to_work, age,
    body_mass_index, education, children, pets...) is a model input feature,
    so one employee is a reusable feature row. ``created_at`` is set once;
    ``updated_at`` is refreshed on every change. Linked to its absence history
    and to the predictions made about it
    """
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    reason_for_absence: Mapped[int] = mapped_column(Integer, nullabe=False)
    absence_date: Mapped[date] = mapped_column(Date, nullable=False)
    input_features: Mapped[dict] = mapped_column(JSON, nullable=False)
    probability: Mapped[float] = mapped_column(Float, nullabe=False)
    is_excessive: Mapped[bool] = mapped_column(Boolean, nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), nullable=False)
    creeated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    employee = relationship("Employee", back_populates="predictions")
