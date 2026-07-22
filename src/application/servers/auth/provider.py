from dishka import Provider, Scope, provide, FromDishka, provide_all
from fastapi import HTTPException, Request
from src.application.servers.auth.encoded_jwt import EncodedJwt
from src.application.servers.auth.decoded_jwt import DecodedJwt
from src.application.schemas.auth import AuthSchema
from loguru import logger


class AuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_token_processor(self) -> DecodedJwt:
        return DecodedJwt()

    @provide(provides=AuthSchema)
    async def get_token_data(
            self,
            processor: FromDishka[DecodedJwt],
            request: FromDishka[Request],
    ) -> AuthSchema:
        logger.info("provider")
        auth_header = request.headers.get("Authorization")
        try:
            return await processor(auth_header)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))
        
    
    
    _get_jwt = provide_all(
        EncodedJwt,
    )