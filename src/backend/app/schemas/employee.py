from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EmployeeBase(BaseModel):
    """
    Shared properties for employee models with validation bounds,
    reused by create/update/out.
    """

    first_name: str = Field(min_length=1, max_length=120)
    last_name: str = Field(min_length=1, max_length=120)
    transportation_expense: float = Field(ge=0)
    distance_to_work: float = Field(ge=0)
    age: int = Field(ge=16, le=100)
    daily_work_load_average: float = Field(ge=0)
    body_mass_index: float = Field(ge=0)
    education: int = Field(ge=0, default=0)
    pets: int = Field(ge=0, default=0)


class EmployeeCreate(EmployeeBase):
    """
    Payload to create an employee (all base fields required)
    """

    pass


class EmployeeUpdate(EmployeeBase):
    """
    Payload for a partial update: every field optional, only sent ones change
    """
    first_name: str | None = Field(default=None, min_length=1, max_length=120)
    last_name: str | None = Field(default=None, min_length=1, max_length=120)
    transportation_expense: float | None = Field(default=None, ge=0)
    distance_to_work: float | None = Field(default=None, ge=0)
    age: int | None = Field(default=None, ge=16, le=100)
    daily_work_load_average: float | None = Field(default=None, ge=0)
    body_mass_index: float | None = Field(default=None, ge=0)
    education: int | None = Field(default=None, ge=1, le=4)
    pets: int | None = Field(default=None, ge=0)


class EmployeeOut(EmployeeBase):
    """
    Employee as returned by the API, with its id and timestamps.
    """

    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime
