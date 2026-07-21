from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, model_validator

from application.schemas.users import CreateUserSchema

class AuthSchema(BaseModel):
    id: UUID = Field(alias="sub")
    role: str = Field(alias="role")


PASSWORD_PATTERN = r"^[A-Za-zА-Яа-я?0-9./_]{8,16}"
class RegistrationSchema(CreateUserSchema):
    password: str = Field(
        min_length=8,
        max_length=16,
        pattern=PASSWORD_PATTERN,
    )
    replay_password: str

    @model_validator(mode="after")
    def validate_passwords_match(self) -> "RegistrationSchema":
        if self.password != self.repeat_password:
            raise ValueError("Пароли не совпадают")

        return self
