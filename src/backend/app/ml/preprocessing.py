"""Feature engineering shared by training and online inference.

"""

from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd

FEATURE_COLUMNS: list[str] = [
    "reason_group_1",
    "reason_group_2",
    "reason_group_3",
    "reason_group_4",
    "month",
    "day_of_week",
    "transportation_expense",
    "distance_to_work",
    "age",
    "daily_work_load_average",
    "body_mass_index",
    "is_higher_education",
    "children",
    "pets",
]

RAW_CSV_COLUMN_MAP = {
    "Reason for Absence": "reason_for_absence",
    "Date": "absence_date",
    "Transportation Expense": "transportation_expense",
    "Distance to Work": "distance_to_work",
    "Age": "age",
    "Daily Work Load Average": "daily_work_load_average",
    "Body Mass Index": "body_mass_index",
    "Education": "education",
    "Children": "children",
    "Pets": "pets",
    "Absenteeism Time in Hours": "absenteeism_time_in_hours",
}


def reason_to_group(reason_code: int) -> int:
    """Map a raw ICD-based absence reason code (0-28) to one of 4 groups.

    Group 1 (1-14): diseases (infectious, neoplasms, mental/nervous system...)
    Group 2 (15-17): pregnancy-related
    Group 3 (18-21): poisoning / external causes
    Group 4 (22-28 and 0): light reasons (consultations, follow-ups, unknown)

    Parameters:
    -----------
    reason_code:
        code of the rease=on of the aemployee'absence
    
    Returns:
        The group of the reason
    """
    if 1 <= reason_code <= 14:
        return 1
    if 15 <= reason_code <= 17:
        return 2
    if 18 <= reason_code <= 21:
        return 3
    return 4


def build_feature_row(
    *,
    reason_for_absence: int,
    absence_date: date,
    transportation_expense: float,
    distance_to_work: float,
    age: int,
    daily_work_load_average: float,
    body_mass_index: float,
    education: int,
    children: int,
    pets: int,
) -> dict:
    """Build a single feature dict, in FEATURE_COLUMNS order, for one absence event."""
    group = reason_to_group(reason_for_absence)
    return {
        "reason_group_1": int(group == 1),
        "reason_group_2": int(group == 2),
        "reason_group_3": int(group == 3),
        "reason_group_4": int(group == 4),
        "month": absence_date.month,
        "day_of_week": absence_date.weekday(),  # 0=Monday ... 6=Sunday
        "transportation_expense": transportation_expense,
        "distance_to_work": distance_to_work,
        "age": age,
        "daily_work_load_average": daily_work_load_average,
        "body_mass_index": body_mass_index,
        # Original dataset encodes education as 1=high school, 2/3/4=higher
        # education. We fold it into a single "has higher education" flag.
        "is_higher_education": int(education != 1),
        "children": children,
        "pets": pets,
    }


def features_to_dataframe(rows: list[dict]) -> pd.DataFrame:
    dataframe = pd.DataFrame(rows)
    return dataframe.reindex(columns=FEATURE_COLUMNS)


def load_raw_dataset(csv_path: str) -> pd.DataFrame:
    """
    Load the original flat CSV (as shipped in data/absenteeism_raw.csv).

    Parameters:
    -----------
    csv_path:
        the original flat csv
    
    Returns:
    --------
     the output dataframe
    """
    dataframe = pd.read_csv(csv_path)
    dataframe = dataframe.drop(columns=["ID"])
    dataframe = dataframe.rename(columns=RAW_CSV_COLUMN_MAP)
    dataframe["absence_date"] = pd.to_datetime(
        dataframe["absence_date"],
        format="%d/%m/%Y"
    ).dt.date
    return dataframe


def preprocess_dataframe(
    df: pd.DataFrame, threshold_hours: float | None = None
) -> tuple[pd.DataFrame, pd.Series, float]:
    """Turn a raw dataframe (one row per historical absence event, with the
    columns produced by `load_raw_dataset` / the DB export) into a model-ready
    feature matrix `X` and binary target `y`.

    "Excessive absenteeism" is defined as more hours than `threshold_hours`
    (the dataset median by default, matching standard practice for this
    dataset rather than an arbitrary fixed cut-off).
    """
    rows = [
        build_feature_row(
            reason_for_absence=int(r.reason_for_absence),
            absence_date=r.absence_date,
            transportation_expense=float(r.transportation_expense),
            distance_to_work=float(r.distance_to_work),
            age=int(r.age),
            daily_work_load_average=float(r.daily_work_load_average),
            body_mass_index=float(r.body_mass_index),
            education=int(r.education),
            children=int(r.children),
            pets=int(r.pets),
        )
        for r in df.itertuples(index=False)
    ]
    X = features_to_dataframe(rows)

    if threshold_hours is None:
        threshold_hours = float(df["absenteeism_time_in_hours"].median())

    y = pd.Series(
        np.where(df["absenteeism_time_in_hours"].to_numpy() > threshold_hours, 1, 0),
        name="is_excessive",
    )
    return X, y, threshold_hours