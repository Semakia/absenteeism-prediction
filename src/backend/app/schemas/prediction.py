from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PredictionRequest(BaseModel):
    """
    Request to score a (possibly hypothetical) absence event

    Either the employee id (uses the employee's stored demographic data) or
    the employee features (a full ad-hoc feature set, for a what-if simulation on
    an employee who doesn't exist yet) must be provided.
    """

    employee_id: int | None = None
    reason_for_absence: int = Field(ge=0, le=28)
    absence_date: date
    manual_features: "ManualEmployeeFeatures | None" = None

    @model_validator(mode="after")
    def check_source(self) -> "PredictionRequest":
        if self.employee_id is None and self.manual_features is None:
            raise ValueError(
                "Provide either employee_id or manual_features"
            )
        return self


class ManualEmployeeFeatures(BaseModel):
    """
    Ad-hoc feature set for a prediction not tied to a stored employees
    """

    transportation_expense: float = Field(ge=0)
    distance_work: float = Field(ge=0)
    distance_to_work: float = Field(ge=0)
    age: int = Field(ge=16, le=100)
    daily_work_load_average: float = Field(ge=0)
    body_mass_index: float = Field(ge=0)
    education: int = Field(ge=0, le=4)
    children: int = Field(ge=0, default=0)
    pets: int = Field(ge=0, default=0)


PredictionRequest.model_rebuild()


class PredictionResult(BaseModel):
    """
    Immediate result returned after scoring (probability + decision + model id)
    """
    probability: float
    is_excessive: bool
    model_version: str


class PredictionOut(BaseModel):
    """
    Prediction as returned by the API, with its id and timestamps.
    """

    model_config = ConfigDict(from_attributes=True)
    id: int
    employee_id: int | None
    reason_for_absence: int
    absence_date: date
    manual_features: ManualEmployeeFeatures | None
    probability: float
    is_excessive: bool
    model_version: str
    created_at: datetime
