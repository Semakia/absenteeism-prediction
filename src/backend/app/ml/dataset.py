import pandas as pd
from sqlalchemy.orm import Session

from app.models.absence_record import AbsenceRecord
from app.maodels.employee import Employee


def build_training_datframe(db: Session) -> pd.DataFrame:
    """Join every historical absence event with its employee's demographic
    data into the flat shape expected by `preprocessing.preprocess_dataframe`.
    """
    rows = (
        db.query(AbsenceRecord, Employee)
        .join(Employee, AbsenceRecord.employee_id == Employee.id)
        .all()
    )
    records = [
        {
            "reason_for_absence": absence.reason_for_absence,
            "absence_date": absence.absence_date,
            "transportation_expense": employee.transportation_expense,
            "distance_to_work": employee.distance_to_work,
            "age": employee.age,
            "daily_work_load_average": employee.daily_work_load_average,
            "body_mass_index": employee.body_mass_index,
            "education": employee.education,
            "children": employee.children,
            "pets": employee.pets,
            "absenteeism_time_in_hours": absence.absenteeism_time_in_hours,
        }
        for absence, employee in rows
    ]
    return pd.DataFrame(records)