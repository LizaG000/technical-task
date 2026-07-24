from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.usecase.base import Usecase
from src.infra.postgres.gateways.base import GetAllGate
from src.infra.postgres.tables import ProductsModel
from dataclasses import dataclass
from src.application.schemas.products import ProductSchema

@dataclass(slots=True, frozen=True, kw_only=True)
class GetAllProductsUsecase(Usecase[None, list[ProductSchema]]):
    session: AsyncSession
    get_all_products: GetAllGate[ProductsModel, ProductSchema]
    
    async def __call__(self, data: None = None) -> list[ProductSchema]:
        async with self.session.begin():
            return await self.get_all_products()
