from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Employee(Base):
    """An employee whose demographic and work data feed the ML model.

    Each column (transportation_expense, distance_to_work, age, body_mass_index,
    education, children, pets...) is a model input feature, so one employee is a
    reusable feature row. ``created_at`` is set once; ``updated_at`` is refreshed
    on every change.
    """

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    transportation_expense: Mapped[float] = mapped_column(Float, nullable=False)
    distance_to_work: Mapped[float] = mapped_column(Float, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_work_load_average: Mapped[float] = mapped_column(Float, nullable=False)
    body_mass_index: Mapped[float] = mapped_column(Float, nullable=False)
    education: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    children: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    pets: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    absence_records = relationship(
        "AbsenceRecord", back_populates="employee", cascade="all, delete-orphan"
    )
    predictions = relationship("Prediction", back_populates="employee")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
