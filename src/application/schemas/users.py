from uuid import UUID
from datetime import datetime, date

from pydantic import Field, field_validator, BaseModel

class UserSchema(BaseModel):
    id: UUID
    first_name: str
    middle_name: str
    last_name: str
    email: str
    birth_date: date
    is_active: bool
    created_at: datetime
    updated_at: datetime


NAME_PATTERN = r"^[A-Za-zА-Яа-я]+(?:[- ][A-Za-zА-Яа-я]+)*$"
EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]{5,}+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$" 
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
    birth_date: date
    is_active: bool

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, value: date) -> date:
        if value > date.today():
            raise ValueError(
                "Дата рождения не может быть в будущем"
            )

        return value
