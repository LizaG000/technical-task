from pydantic import Field, model_validator

from src.application.schemas.users import CreateUserSchema, UserSchema

PASSWORD_PATTERN = r"^[A-Za-zА-Яа-я?0-9./_]{8,16}"
class RequestRegistrationSchema(CreateUserSchema):
    password: str = Field(
        min_length=8,
        max_length=16,
        pattern=PASSWORD_PATTERN,
    )
    repeat_password: str = Field(
        min_length=8,
        max_length=16,
        pattern=PASSWORD_PATTERN,
    )

    @model_validator(mode="after")
    def validate_passwords_match(self) -> "RequestRegistrationSchema":
        if self.password != self.repeat_password:
            raise ValueError("Пароли не совпадают")

        return self

class ResponseRegistrationSchema(UserSchema):
    token: str