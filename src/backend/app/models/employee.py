
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.databse import Base


class Employee(Base):
    """
    This class means the table of employees (features of the model)
    """

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(120))
    last_name: Mapped[str]  = mapped_column(Float, nullable=False)
    transportation_expense: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    distance_work: Mapped[float] = mapped_column(Float, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    daily_work_load_average: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    body_mass_index: Mapped[float] = mapped_column(Float, nullable=False)
    children: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    absence_records = relationship(
        "AbsenceRecord",
        back_populates="employee",
        cascade="all, delete-orphan"
    )

    predictions = relationship(
        "Prediction",
        back_populates="employee"
    )

    @propoerty
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
