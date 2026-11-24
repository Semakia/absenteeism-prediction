"""Initial schema

Revision ID: 0001
Revises:
Create Date: 2026-09-01
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column(
            "role",
            sa.String(length=50),
            nullable=False,
            server_default="hr_manager",
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "employees",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("first_name", sa.String(length=120), nullable=False),
        sa.Column("last_name", sa.String(length=120), nullable=False),
        sa.Column("transportation_expense", sa.Float(), nullable=False),
        sa.Column("distance_to_work", sa.Float(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("daily_work_load_average", sa.Float(), nullable=False),
        sa.Column("body_mass_index", sa.Float(), nullable=False),
        sa.Column("education", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("children", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("pets", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "absence_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "employee_id",
            sa.Integer(),
            sa.ForeignKey("employees.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("reason_for_absence", sa.Integer(), nullable=False),
        sa.Column("absence_date", sa.Date(), nullable=False),
        sa.Column("absenteeism_time_in_hours", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_absence_records_employee_id", "absence_records", ["employee_id"]
    )

    op.create_table(
        "model_versions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("version", sa.String(length=50), nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column("n_train_samples", sa.Integer(), nullable=False),
        sa.Column("n_test_samples", sa.Integer(), nullable=False),
        sa.Column("accuracy", sa.Float(), nullable=False),
        sa.Column("precision", sa.Float(), nullable=False),
        sa.Column("recall", sa.Float(), nullable=False),
        sa.Column("f1_score", sa.Float(), nullable=False),
        sa.Column("roc_auc", sa.Float(), nullable=False),
        sa.Column("artifact_path", sa.String(length=500), nullable=False),
        sa.Column("trained_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_model_versions_version", "model_versions", ["version"], unique=True
    )

    op.create_table(
        "predictions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "employee_id",
            sa.Integer(),
            sa.ForeignKey("employees.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "requested_by_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("reason_for_absence", sa.Integer(), nullable=False),
        sa.Column("absence_date", sa.Date(), nullable=False),
        sa.Column("input_features", sa.JSON(), nullable=False),
        sa.Column("probability", sa.Float(), nullable=False),
        sa.Column("is_excessive", sa.Boolean(), nullable=False),
        sa.Column("model_version", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("predictions")
    op.drop_index("ix_model_versions_version", table_name="model_versions")
    op.drop_table("model_versions")
    op.drop_index(
        "ix_absence_records_employee_id", table_name="absence_records"
    )
    op.drop_table("absence_records")
    op.drop_table("employees")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
