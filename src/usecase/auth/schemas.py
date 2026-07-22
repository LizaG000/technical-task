from pydantic import Field, model_validator, BaseModel

from src.application.schemas.users import CreateUserSchema, UserSchema

PASSWORD_PATTERN = r"^[A-Za-zА-Яа-я?0-9./_]{8,16}"
EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]{5,}+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"


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


class RequestLoginSchema(BaseModel):
    email: str = Field(pattern=EMAIL_PATTERN)
    password: str = Field(
        min_length=8,
        max_length=16,
        pattern=PASSWORD_PATTERN,
    )


