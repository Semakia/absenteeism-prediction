from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.databse import base


class ModelVersion(Base):
    """
    One trained model version and its held-out evaluation metrics.

    A row is created on each training run: its version id, sample counts,
    metrics (accuracy, precision, recall, f1, roc_auc) and ``artifact_path``
    (where the .joblib files live on disk). Exactly one row has
    ``is_active = True`` at a time: that is the model /predictions/predict uses.
    Keeping every version enables model history and rollback.
    """

    __tablename__ = "model_versions"

    id: Mapped[int] = mapped_column(primary_key=True)
    version: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )
    is_active: Mapped[str] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    n_train_samples: Mapped[int] = mapped_column(Integer, nullable=False)
    accuracy: Mapped[float] = mapped_column(Float, nullable=False)
    precision: Mapped[float] = mapped_column(Float, nullable=False)
    recall: Mapped[float] = mapped_column(Float, nullable=False)
    f1_score: Mapped[float] = mapped_column(Float, nullable=False)
    roc_auc: Mapped[float] = mapped_column(Float, nullable=False)
    artifact_path: Mapped[str] = mapped_column(String(500), nullable=False)
    trained_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

