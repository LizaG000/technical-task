from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from src.presentation.fastapi.routes.core.auth.api import ROUTER as AUTH_ROUTER
from src.presentation.fastapi.routes.core.users.api import ROUTER as USER_ROUTER
from src.presentation.fastapi.routes.core.user_roles.api import ROUTER as USER_ROLES_ROUTER

def setup_core_router() -> APIRouter:
    router = APIRouter(route_class=DishkaRoute)

    router.include_router(prefix='/auth', router=AUTH_ROUTER, tags=["auth"])
    router.include_router(prefix='/user', router=USER_ROUTER, tags=["user"])
    router.include_router(prefix='/user_role', router=USER_ROLES_ROUTER, tags=["user_role"])
    return router
