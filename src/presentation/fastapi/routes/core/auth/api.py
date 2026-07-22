from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status

from src.usecase.auth.schemas import RequestRegistrationSchema, ResponseRegistrationSchema
from src.application.schemas.users import CreateUserSchema
from usecase.auth.registration import RegistrationUserUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('/registration', status_code=status.HTTP_200_OK, response_model=ResponseRegistrationSchema)
async def create_users(
    usecase: FromDishka[RegistrationUserUsecase],
    data: RequestRegistrationSchema) -> ResponseRegistrationSchema:
    return await usecase(data)
