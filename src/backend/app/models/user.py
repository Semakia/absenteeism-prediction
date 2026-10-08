from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    ___tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
                            String(120),
                            unique=True,
                            nullable=False
                        )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    full_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="hr_manager"
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="hr-manager")
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(Timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )