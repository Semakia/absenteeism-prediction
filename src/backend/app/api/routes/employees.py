from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database import get_db
from app.models.employee import Employee
from app.models.user import User
from app.schemas.employee import EmployeeCreate, EmployeeOut, EmployeeUpdate

router = APIRouter(prefix="/employees", tags=["employees"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[EmployeeOut])
def list_employees(
    db: Session = Depends(get_db),
    search: str | None = Query(default=None, description="Filter by first/last name"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    """List employees, optionally filtered by name, with pagination."""
    query = db.query(Employee)
    if search:
        like = f"%{search}%"
        query = query.filter((Employee.first_name.ilike(like)) | (Employee.last_name.ilike(like)))
    return query.order_by(Employee.id).offset(offset).limit(limit).all()


@router.post("", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    """Create a new employee."""
    employee = Employee(**payload.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def _get_employee_or_404(employee_id: int, db: Session) -> Employee:
    employee = db.get(Employee, employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Fetch a single employee by id."""
    return _get_employee_or_404(employee_id, db)


@router.put("/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, payload: EmployeeUpdate, db: Session = Depends(get_db)):
    """Partially update an employee (only the fields provided)."""
    employee = _get_employee_or_404(employee_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)
    db.commit()
    db.refresh(employee)
    return employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Delete an employee (and, by cascade, its absence records)."""
    employee = _get_employee_or_404(employee_id, db)
    db.delete(employee)
    db.commit()
