from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter
from fastapi import status

from src.usecase.auth.schemas import RequestRegistrationSchema, ResponseRegistrationSchema, RequestLoginSchema
from src.application.schemas.users import CreateUserSchema
from src.usecase.auth.registration import RegistrationUserUsecase
from src.usecase.auth.login import LoginUserUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.post('/registration', status_code=status.HTTP_200_OK, response_model=ResponseRegistrationSchema)
async def registration_users(
    usecase: FromDishka[RegistrationUserUsecase],
    data: RequestRegistrationSchema) -> ResponseRegistrationSchema:
    return await usecase(data)

@ROUTER.post('/login', status_code=status.HTTP_200_OK, response_model=ResponseRegistrationSchema)
async def login_users(
    usecase: FromDishka[LoginUserUsecase],
    data: RequestLoginSchema) -> ResponseRegistrationSchema:
    return await usecase(data)
