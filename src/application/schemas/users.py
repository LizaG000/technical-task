from uuid import UUID
from datetime import datetime, timezone

from pydantic import Field, BaseModel

NAME_PATTERN = r"^[A-Za-zА-Яа-я]+(?:[- ][A-Za-zА-Яа-я]+)*$"
EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]{5,}+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

class UserSchema(BaseModel):
    id: UUID
    first_name: str
    middle_name: str
    last_name: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

 
class CreateUserSchema(BaseModel):
    first_name: str = Field(
        min_length=2,
        max_length=50,
        pattern=NAME_PATTERN,
    )
    middle_name: str = Field(
        min_length=2,
        max_length=50,
        pattern=NAME_PATTERN,
    )
    last_name: str = Field(
        min_length=2,
        max_length=50,
        pattern=NAME_PATTERN,
    )
    email: str = Field(pattern=EMAIL_PATTERN)

class UserRoleSchema(UserSchema):
    role: str


class UpdateUserSchema(BaseModel):
    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
        pattern=NAME_PATTERN,
    )
    middle_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
        pattern=NAME_PATTERN,
    )
    last_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
        pattern=NAME_PATTERN,
    )
    updated_at: datetime = datetime.now(timezone.utc)
