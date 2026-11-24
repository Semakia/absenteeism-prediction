"""Idempotent startup bootstrap: run once (e.g. from the container entrypoint)
after migrations have been applied.

- Ensures an initial HR admin account exists.
- Imports the bundled historical dataset if the database is still empty.
- Trains and activates a first model version if none exists yet, so the
  API is immediately usable after a fresh deploy instead of returning
  503 from /predictions/predict until someone remembers to call /data/train.
"""
import logging

from app.config import get_settings
from app.core.security import hash_password
from app.database import SessionLocal
from app.ml.dataset import build_training_dataframe
from app.ml.importer import import_raw_csv
from app.ml.train import train_and_evaluate
from app.models.employee import Employee
from app.models.model_version import ModelVersion
from app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("seed")
settings = get_settings()


def seed_admin_user(db) -> None:
    """Create the initial admin account if it does not exist yet."""
    existing = db.query(User).filter(User.email == settings.initial_admin_email).first()
    if existing:
        logger.info("Admin user already exists, skipping.")
        return
    db.add(
        User(
            email=settings.initial_admin_email,
            hashed_password=hash_password(settings.initial_admin_password),
            full_name=settings.initial_admin_full_name,
            role="admin",
        )
    )
    db.commit()
    logger.info("Created initial admin user: %s", settings.initial_admin_email)


def seed_historical_dataset(db) -> None:
    """Import the bundled CSV once, only if no employee exists yet."""
    if db.query(Employee).count() > 0:
        logger.info("Employees table already has data, skipping CSV import.")
        return
    if not settings.raw_dataset_path.exists():
        logger.warning("Raw dataset not found at %s, skipping import.", settings.raw_dataset_path)
        return
    imported = import_raw_csv(db, settings.raw_dataset_path.read_bytes())
    logger.info("Imported %d historical absence records.", imported)


def seed_initial_model(db) -> None:
    """Train and activate a first model if none is active yet."""
    if db.query(ModelVersion).filter(ModelVersion.is_active.is_(True)).first():
        logger.info("An active model already exists, skipping training.")
        return
    df = build_training_dataframe(db)
    if len(df) < 20:
        logger.warning("Not enough data (%d rows) to train an initial model, skipping.", len(df))
        return
    result = train_and_evaluate(df, settings.ml_artifacts_dir)
    db.add(
        ModelVersion(
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
    )
    db.commit()
    logger.info(
        "Trained initial model %s (accuracy=%.3f, f1=%.3f)",
        result.version,
        result.accuracy,
        result.f1_score,
    )


def main() -> None:
    """Run all bootstrap steps in order, in a single DB session."""
    db = SessionLocal()
    try:
        seed_admin_user(db)
        seed_historical_dataset(db)
        seed_initial_model(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
