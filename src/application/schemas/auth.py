from uuid import UUID
from pydantic import BaseModel, Field

class AuthSchema(BaseModel):
    id: UUID = Field(alias="sub")
    role: list[str] = Field(alias="role")
    jti: UUID = Field(alias="jti")
    expire: int = Field(alias="expire")


