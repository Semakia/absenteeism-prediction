from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    """
    Payload to create an HR account 
    """

    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    role: str = "hr_manager"


class UserOut(BaseModel):
    """
    Public view of a user returned by the API (never express the password hash)
    """
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    full_name: str
    role: str
    is_active: bool


class Token(BaseModel):
    """
    Token model for authentication responses.
    """
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    Decoded JWT claims we care about (the subject = user id).
    """
    sub: str | None = None