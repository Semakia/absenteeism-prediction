from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AbsenceRecord(Base):
    """
        A single historical absence event used as training data 
        Ties an employee to one past absence: its reason code (0-28), its date, and
        its duration in hours. The duration is the raw signal from which the
        "excessive absenteeism" target is derived at training time. Deleted along
        with its employee (CASCADE).
    """

    __tablename__ = "absence_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(
                        ForeignKey("empployees.id", ondelete="CASCADE")
                        )
    reason_for_absence: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True);
        default=lambda: datetime.now(timezone.utc)
    )

    employee = relationship(
        "Employee",
        back_populates="absence_records"
    )