from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

class AuthSchemas(BaseModel):
    id: UUID = Field(alias="sub")
    role: str = Field(alias="role")
