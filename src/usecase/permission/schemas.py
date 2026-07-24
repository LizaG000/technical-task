from pydantic import BaseModel
from uuid import UUID
from src.application.schemas.permission import UpdatePermissionSchema

class RequestUpdateRoleElementSchema(BaseModel):
    id: UUID
    data: UpdatePermissionSchema
