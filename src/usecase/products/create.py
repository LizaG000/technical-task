from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import CreateReturningGate
from src.infra.postgres.tables import ProductsModel
from dataclasses import dataclass
from src.application.schemas.products import ProductSchema, CreateProductSchema
from src.application.schemas.auth import AuthSchema
from src.application.servers.auth.check_is_active import CheckIsActive
from src.infra.postgres.gateways.roles import GetAccessRightsGate
from src.application.enums.elements import Elements
from src.application.enums.method import Methods

@dataclass(slots=True, frozen=True, kw_only=True)
class CreateProductUsecase(Usecase[CreateProductSchema, ProductSchema]):
    session: AsyncSession
    auth: AuthSchema
    create_product: CreateReturningGate[ProductsModel, CreateReturningGate, ProductSchema]
    check_is_active: CheckIsActive
    get_access_rights: GetAccessRightsGate
    
    async def __call__(self, data: CreateProductSchema) -> ProductSchema:
        async with self.session.begin():
            await self.check_is_active(self.auth.id)
            await self.get_access_rights(self.auth.id, Elements.PRODUCT.value, Methods.CREATE.value)
            return await self.create_product(data)
