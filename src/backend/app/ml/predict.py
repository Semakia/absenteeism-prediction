from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import joblib
from app.ml.preprocessing import build_feature_row, features_to_dataframe
from app.ml.train import METADATA_FILENAME, MODEL_FILENAME, SCALER_FILENAME


@dataclass
class ModelBundle:
    """Everything required to score a single absence event at inference time.

    Grouping these together keeps the model, its scaler and its metadata in
    sync: they were produced together during training and must always be used
    together.

    Attributes:
    -----------
    version:
        Version string of the trained model, read from the metadata file.
    model:
        The fitted scikit-learn estimator (logistic regression).
    scaler:
        The fitted ``StandardScaler`` used during training. The exact same
        scaler must be applied at inference, otherwise the features are on a
        different scale than the model was trained on.
    feature_columns:
        Ordered list of feature column names expected by the model.
    threshold_hours:
        Absence-hours cut-off used to label "excessive absenteeism" when the
        model was trained (kept for reference / reproducibility).
    """

    version: str
    model: object
    scaler: object
    feature_columns: list[str]
    threshold_hours: float


_bundle_cache: dict[str, ModelBundle] = {}


def load_model_bundle(artifact_dir: str | Path) -> ModelBundle:
    """Load a trained model bundle from a directory of artifacts.

    Reads the metadata JSON and deserializes the model and scaler produced by
    the training step. Results are cached per directory in a module-level
    dict, so repeated calls with the same ``artifact_dir`` return the already
    loaded bundle instead of reading the files again (useful when an API
    serves many requests).

    Parameters:
    -----------
    artifact_dir:
        Path to the directory containing ``metadata.json``, the serialized
        model and the serialized scaler.

    Returns:
    --------
    ModelBundle
        The loaded bundle, ready to be passed to :func:`predict_one`.
    """
    artifact_dir = Path(artifact_dir)
    cache_key = str(artifact_dir)
    if cache_key in _bundle_cache:
        return _bundle_cache[cache_key]

    metadata = json.loads((artifact_dir / METADATA_FILENAME).read_text())
    bundle = ModelBundle(
        version=metadata["version"],
        model=joblib.load(artifact_dir / MODEL_FILENAME),
        scaler=joblib.load(artifact_dir / SCALER_FILENAME),
        feature_columns=metadata["feature_columns"],
        threshold_hours=metadata["threshold_hours"]  
    )
    _bundle_cache[cache_key] = bundle
    return bundle


def predict_one(
    bundle: ModelBundle,
    *,
    reason_for_absence: str,
    absence_date: date,
    transportation_expense: float,
    distance_to_work: float,
    age: int,
    daily_work_load_average: float,
    body_mass_index: float,
    education: str,
    children: int,
    pets: int
) -> tuple[float, bool]:
    """Score a single absence event and return its excessive-absenteeism risk.

    Builds the feature row with the same transformations used at training
    time, applies the fitted scaler, and runs the model to get the predicted
    probability of the "excessive absenteeism" class.

    Parameters:
    -----------
    bundle:
        The trained model bundle, as returned by :func:`load_model_bundle`.
    reason_for_absence:
        Raw ICD-based absence reason code (0-28); grouped internally into one
        of 4 reason groups.
    absence_date:
        Date of the absence; its month and weekday are used as features.
    transportation_expense:
        Monthly transportation expense of the employee.
    distance_to_work:
        Distance from home to work (same unit as the training data).
    age:
        Age of the employee, in years.
    daily_work_load_average:
        Average daily workload at the time of the absence.
    body_mass_index:
        Body mass index of the employee.
    education:
        Education level (1 = high school, 2/3/4 = higher education); folded
        into a single "higher education" flag internally.
    children:
        Number of children of the employee.
    pets:
        Number of pets of the employee.

    Returns:
    --------
    tuple[float, bool]
        A ``(probability, is_excessive)`` pair, where ``probability`` is the
        predicted probability of excessive absenteeism (between 0 and 1) and
        ``is_excessive`` is ``True`` when that probability is at least 0.5.
    """
    row = build_feature_row(
        reason_for_absence=reason_for_absence,
        absence_date=absence_date,
        transportation_expense=transportation_expense,
        distance_to_work=distance_to_work,
        age=age,
        daily_work_load_average=daily_work_load_average,
        body_mass_index=body_mass_index,
        education=education,
        children=children,
        pets=pets
    )
    X = features_to_dataframe([row])
    X_scaled = bundle.scaler.transform(X)
    probability = float(bundle.model.predict_proba(X_scaled)[0, 1])
    is_excessive = probability >= 0.5
    return probability, is_excessive
