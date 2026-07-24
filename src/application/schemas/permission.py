from uuid import UUID
from datetime import datetime, date, timezone

from pydantic import BaseModel

class PermissionSchema(BaseModel):
    id: UUID
    role: str
    element: str
    create: bool
    patch: bool
    get: bool
    get_all: bool
    delete: bool
    created_at: datetime
    updated_at: datetime


class UpdatePermissionSchema(BaseModel):
    create: bool | None = None
    patch: bool | None = None
    get: bool | None = None
    get_all: bool | None = None
    delete: bool | None = None
    updated_at: datetime = datetime.now(timezone.utc)
    
