from io import BytesIO

import pandas as pd
from sqlalchemy.orm import Session

from app.ml.preprocessing import RAW_CSV_COLUMN_MAP
from app.models.absence_record import AbsenceRecord
from app.models.employee import Employee

# Sensible neutral defaults used only if a legacy row was somehow missing them.
_DEFAULT_EDUCATION = 1


def import_raw_csv(db: Session, file_bytes: bytes) -> int:
    """Import a CSV shaped like the original `Absenteeism-data.csv` export.

    Each row becomes one Employee (the flat legacy export has no stable
    employee identity beyond a per-row anonymized ID) plus one AbsenceRecord
    tied to it. Returns the number of absence records imported.

    Args:
    -----
        db (Session): SQLAlchemy session to use for the import.
        file_bytes (bytes): Raw bytes of the CSV file.
    Returns:
    -------
        int: Number of absence records imported.
    """
    df = pd.read_csv(BytesIO(file_bytes))
    df = df.rename(columns=RAW_CSV_COLUMN_MAP)
    df["absence_date"] = pd.to_datetime(df["absence_date"], format="%d/%m/%Y").dt.date

    imported = 0
    for row in df.itertuples(index=False):
        employee = Employee(
            first_name="Imported",
            last_name=f"Employee #{getattr(row, 'ID', imported + 1)}",
            transportation_expense=float(row.transportation_expense),
            distance_to_work=float(row.distance_to_work),
            age=int(row.age),
            daily_work_load_average=float(row.daily_work_load_average),
            body_mass_index=float(row.body_mass_index),
            education=int(row.education) if not pd.isna(row.education) else _DEFAULT_EDUCATION,
            children=int(row.children),
            pets=int(row.pets),
        )
        db.add(employee)
        db.flush()  # assign employee.id without committing yet
        db.add(
            AbsenceRecord(
                employee_id=employee.id,
                reason_for_absence=int(row.reason_for_absence),
                absence_date=row.absence_date,
                absenteeism_time_in_hours=int(row.absenteeism_time_in_hours),
            )
        )
        imported += 1

    db.commit()
    return imported
