from uuid import UUID
from datetime import datetime, date

from pydantic import BaseModel

class UserRoleSchema(BaseModel):
    id: UUID
    user_id: UUID
    role: str
    created_at: datetime
    updated_at: datetime
    
class CreateUserRoleSchema(BaseModel):
    user_id: UUID
    role: str
    
class GetUserRoleSchema(BaseModel):
    user_id: UUID
