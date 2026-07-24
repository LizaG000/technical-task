from pydantic import BaseModel
from datetime import datetime, timezone
from uuid import UUID

class ProductSchema(BaseModel):
    id: UUID
    name:str
    description:str
    price:float
    count:int
    created_at:datetime
    updated_at:datetime


class CreateProductSchema(BaseModel):
    name:str
    description:str
    price:float
    count:int


class UpdateProductSchema(BaseModel):
    name:str | None = None
    description:str | None = None
    price:float | None = None
    count:int | None = None
    created_at:datetime | None = None
