from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status

from src.usecase.users.schemas import RequestRegistrationSchema, ResponseRegistrationSchema
from src.application.schemas.users import CreateUserSchema
from src.usecase.users.create import CreateUserUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('', status_code=status.HTTP_200_OK, response_model=ResponseRegistrationSchema)
async def create_users(
    usecase: FromDishka[CreateUserUsecase],
    data: RequestRegistrationSchema) -> ResponseRegistrationSchema:
    return await usecase(data)
