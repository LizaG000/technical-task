from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi import status

from src.application.schemas.user_role import CreateUserRoleSchema, UserRoleSchema
from src.usecase.user_roles.create import CreateUserRoleUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=UserRoleSchema, dependencies=[Depends(HTTPBearer())])
async def update_user(
    usecase: FromDishka[CreateUserRoleUsecase],
    data: CreateUserRoleSchema) -> UserRoleSchema:
    return await usecase(data)
