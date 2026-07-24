from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from fastapi import status
from src.application.schemas.permission import PermissionSchema
from src.usecase.permission.schemas import RequestUpdateRoleElementSchema
from src.usecase.permission.get_all import GetAllPermissionUsecase
from src.usecase.permission.update import UpdatePermissionUsecase
ROUTER = APIRouter(route_class=DishkaRoute)

@ROUTER.patch('', status_code=status.HTTP_200_OK, response_model=PermissionSchema, dependencies=[Depends(HTTPBearer())])
async def update_permission(
    usecase: FromDishka[UpdatePermissionUsecase],
    data: RequestUpdateRoleElementSchema) -> PermissionSchema:
    return await usecase(data)


@ROUTER.get('', status_code=status.HTTP_200_OK, response_model=list[PermissionSchema], dependencies=[Depends(HTTPBearer())])
async def get_all_permission(
    usecase: FromDishka[GetAllPermissionUsecase]) -> list[PermissionSchema]:
    return await usecase()
