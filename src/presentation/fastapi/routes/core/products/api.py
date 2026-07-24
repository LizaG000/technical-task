from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi import status
from src.application.schemas.products import ProductSchema, CreateProductSchema
from src.usecase.products.get_all import GetAllProductsUsecase
from src.usecase.products.create import CreateProductUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.get('/all', status_code=status.HTTP_200_OK, response_model=list[ProductSchema])
async def get_all_product(
    usecase: FromDishka[GetAllProductsUsecase]) -> list[ProductSchema]:
    return await usecase()

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=ProductSchema)
async def create_product(
    usecase: FromDishka[CreateProductUsecase],
    data: CreateProductSchema) -> ProductSchema:
    return await usecase(data)
