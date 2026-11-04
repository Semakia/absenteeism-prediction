from pydantic import BaseModel


class ReasonGroupBreakdown(BaseModel):
    """
    Count of absence records grouped by reason group
    """

    reason_group: int
    count: int


class MonthlyAverage(BaseModel):
    """
    Average abcsence hours for a given month number (1-12)
    """
    month: int
    average_hours: float


class ModelInfo(BaseModel):
    """
    Summary of the active model's metrics for the dashboard.
    """

    version: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    trained_at: str


class DashboardStats(BaseModel):
    """
    Aggregated figures powering the dashboard view.
    """

    total_employees: int
    total_predictions: int
    total_absence_records: int
    excessive_rate: float
    reason_breakdown: list(ReasonGroupBreakdown)
    monthly_average_hours: list(MonthlyAverage)
    active_model: ModelInfo | None
