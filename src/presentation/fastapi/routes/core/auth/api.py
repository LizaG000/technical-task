from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Depends
from fastapi import status
from fastapi.security import HTTPBearer

from src.usecase.auth.schemas import RequestRegistrationSchema, ResponseRegistrationSchema, RequestLoginSchema
from src.usecase.auth.registration import RegistrationUserUsecase
from src.usecase.auth.login import LoginUserUsecase
from src.usecase.auth.logout import LogoutUserUsecase
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


@ROUTER.post('/logout', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(HTTPBearer())])
async def login_users(
    usecase: FromDishka[LogoutUserUsecase]) -> None:
    return await usecase()
