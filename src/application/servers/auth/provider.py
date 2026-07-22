from dishka import Provider, Scope, provide, FromDishka, provide_all
from fastapi import HTTPException, Request
from src.application.servers.auth.encoded_jwt import EncodedJwt
from src.application.servers.auth.decoded_jwt import DecodedJwt
from src.application.schemas.auth import AuthSchema
from src.config import AuthConfig
from loguru import logger


class AuthProvider(Provider):
    scope = Scope.REQUEST
    
    _get_jwt = provide_all(
        EncodedJwt,
        DecodedJwt,
    )

    @provide(provides=AuthSchema)
    async def get_token_data(
            self,
            processor: FromDishka[DecodedJwt],
            request: FromDishka[Request],
    ) -> AuthSchema:
        auth_header = request.headers.get("Authorization")
        token = auth_header.removeprefix("Bearer ").strip()
        try:
            return await processor(token)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))
        
    
    