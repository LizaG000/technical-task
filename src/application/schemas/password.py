from uuid import UUID
from datetime import datetime, date

from pydantic import BaseModel

class PasswordSchema(BaseModel):
    id: UUID
    user_id: UUID
    password: str
    created_at: datetime
    updated_at: datetime
    
class CreatePasswordSchema(BaseModel):
    user_id: UUID
    password: str
