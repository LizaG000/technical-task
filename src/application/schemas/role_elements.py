from uuid import UUID
from datetime import datetime, date

from pydantic import BaseModel

class RoleElementsSchema(BaseModel):
    id: UUID
    user_id: UUID
    role: str
    element: str
    create: bool
    patch: bool
    get: bool
    get_all: bool
    delete: bool
    created_at: datetime
    updated_at: datetime
    
