from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi import status

from src.application.schemas.users import UpdateUserSchema, UserSchema
from src.usecase.users.update import UpdateUserUsecase
ROUTER = APIRouter(route_class=DishkaRoute)
security = HTTPBearer()

@ROUTER.patch('', status_code=status.HTTP_200_OK, response_model=UserSchema, dependencies=[Depends(security)])
async def registration_users(
    usecase: FromDishka[UpdateUserUsecase],
    data: UpdateUserSchema) -> UserSchema:
    return await usecase(data)