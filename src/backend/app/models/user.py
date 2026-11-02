from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    """
    An HR account allowed to authenticate and use the API.

    Stores credentials (as a bcrypt hash, never plaintext) and the account
    state. ``is_active`` lets an account be disabled without being deleted;
    login is refused when it is False.
    """
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
    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="hr-manager"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(Timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
