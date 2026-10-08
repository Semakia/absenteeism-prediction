from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App settingd
    app_name: str = "Absenteeism Prediction API"
    environment: str = "development"
    api_prefix: str = "/api/v1"

    # Security settings
    secret_key: str = "CHANGE_ME_IN_PRODUCTION"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 8

    # CORS
    cors_origins: list[str] = ["http://localhost:4200"]

    # Database
    database_url: str = "postgresql+psycopg2://absenteeism:absenteeism@localhost:5432/absenteeism"

    # Seed
    initial_admin_email: str = "admin@example.com"
    initial_admin_password: str = "ChangeMe123!"
    initial_admin_full_name: str = "HR Administrator"

    # ML artifacts
    ml_artifacts_dir: Path = BACKEND_ROOT / "app" / "ml" / "artifacts"
    raw_dataset_path: Path = BACKEND_ROOT / "data" / "absenteeism_raw.csv"
    excessive_absenteeism_threshold_mode: str = "median"  # "median" or a float number of hours


@lru_cache
def get_settings() -> Settings:
    return Settings()