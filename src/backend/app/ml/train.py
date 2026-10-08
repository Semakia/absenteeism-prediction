"""Model training & evaluation.

Replaces the original `scripts/processing.py` prototype, fixing two bugs:
the median threshold used to define "excessive absenteeism" was computed
but never actually applied (a hard-coded `> 3` was used instead), and the
model was scored on the training set only. Here the threshold is applied
end-to-end and the reported metrics come from the held-out test split.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from app.ml.preprocessing import FEATURE_COLUMNS, preprocess_dataframe

MODEL_FILENAME = "model.joblib"
SCALER_FILENAME = "scaler.joblib"
METADATA_FILENAME = "metadata.json"


@dataclass
class TrainingResult:
    """Summary of a single training run and where its artifacts were saved.

    Attributes:
    -----------
    version:
        Version identifier of the run (a UTC timestamp), also used as the
        artifact sub-directory name.
    artifact_dir:
        Directory where the model, scaler and metadata were written.
    n_train_samples:
        Number of samples in the training split.
    n_test_samples:
        Number of samples in the held-out test split.
    accuracy:
        Accuracy on the test split.
    precision:
        Precision on the test split (positive class = excessive absenteeism).
    recall:
        Recall on the test split.
    f1_score:
        F1 score on the test split.
    roc_auc:
        ROC AUC on the test split, computed from predicted probabilities.
    threshold_hours:
        Absence-hours cut-off used to label the "excessive" class.
    """

    version: str
    artifact_dir: Path
    n_train_samples: int
    n_test_samples: int
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    threshold_hours: float


def train_and_evaluate(
    raw_df: pd.DataFrame,
    artifacts_root: Path,
    random_state: int = 20,
    test_size: float = 0.2,
) -> TrainingResult:
    """Train a logistic regression model, evaluate it, and persist artifacts.

    Builds the feature matrix and target from the raw data, splits it into a
    stratified train/test set, scales the features, fits the model, scores it
    on the held-out test split, and writes the model, scaler and metadata to a
    timestamped sub-directory of ``artifacts_root``.

    Parameters:
    -----------
    raw_df:
        Raw dataframe with one row per historical absence event, as produced
        by ``load_raw_dataset`` or the database export. Must contain at least
        20 records.
    artifacts_root:
        Root directory under which a timestamped artifact sub-directory is
        created for this run.
    random_state:
        Seed passed to the train/test split for reproducible results.
    test_size:
        Fraction of the data held out for evaluation (e.g. 0.2 = 20%).

    Returns:
    --------
    TrainingResult
        Metrics for the run plus the path where the artifacts were saved.

    Raises:
    -------
    ValueError
        If ``raw_df`` contains fewer than 20 records.
    """
    if len(raw_df) < 20:
        raise ValueError("""Not enough historical absence records
         to train a model (need >= 20).""")

    X, y, threshold_hours = preprocess_dataframe(raw_df)

    train_X, test_X, train_y, test_y = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    scaler = StandardScaler()
    train_X_scaled = scaler.fit_transform(train_X)
    test_X_scaled = scaler.transform(test_X)

    model = LogisticRegression(max_iter=1000)
    model.fit(train_X_scaled, train_y)

    predictions = model.predict(test_X_scaled)
    probabilities = model.predict_proba(test_X_scaled)[:, 1]

    version = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    artifact_dir = artifacts_root / version
    artifact_dir.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, artifact_dir / MODEL_FILENAME)
    joblib.dump(scaler, artifact_dir / SCALER_FILENAME)
    metadata = {
        "version": version,
        "feature_columns": FEATURE_COLUMNS,
        "threshold_hours": threshold_hours,
    }
    (artifact_dir / METADATA_FILENAME).write_text(
        json.dumps(metadata, indent=2)
        )

    return TrainingResult(
        version=version,
        artifact_dir=artifact_dir,
        n_train_samples=len(train_X),
        n_test_samples=len(test_X),
        accuracy=accuracy_score(test_y, predictions),
        precision=precision_score(test_y, predictions, zero_division=0),
        recall=recall_score(test_y, predictions, zero_division=0),
        f1_score=f1_score(test_y, predictions, zero_division=0),
        roc_auc=roc_auc_score(test_y, probabilities),
        threshold_hours=threshold_hours,
    )
