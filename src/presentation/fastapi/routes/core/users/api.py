from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi import status

from src.application.schemas.users import UpdateUserSchema, UserSchema
from src.usecase.users.update import UpdateUserUsecase
from src.usecase.users.delete import DeleteUserUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.patch('', status_code=status.HTTP_200_OK, response_model=UserSchema, dependencies=[Depends(HTTPBearer())])
async def update_user(
    usecase: FromDishka[UpdateUserUsecase],
    data: UpdateUserSchema) -> UserSchema:
    return await usecase(data)

@ROUTER.delete('', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(HTTPBearer())])
async def delete_user(
    usecase: FromDishka[DeleteUserUsecase]) -> None:
    return await usecase()