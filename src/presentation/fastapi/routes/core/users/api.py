from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi import status

from src.application.schemas.user_role import GetUserRoleSchema
from src.application.schemas.users import UpdateUserSchema, UserSchema, UserRoleSchema
from src.usecase.users.update import UpdateUserUsecase
from src.usecase.users.delete import DeleteUserUsecase
from src.usecase.users.get import GetUserRoleUsecase
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


@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=UserRoleSchema, dependencies=[Depends(HTTPBearer())])
async def get_user(
    usecase: FromDishka[GetUserRoleUsecase],
    data: UUID) -> UserRoleSchema:
    return await usecase(data)
