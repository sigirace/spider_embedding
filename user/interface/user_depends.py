from fastapi import Depends
from dependency_injector.wiring import Provide, inject
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from containers import Container
from user.application.token_service import TokenService
from user.domain.user import User

security = HTTPBearer()


@inject
async def get_current_user(
    cred: HTTPAuthorizationCredentials = Depends(security),
    token_service: TokenService = Depends(Provide[Container.token_service]),
) -> User:
    return token_service.validate_token(cred.credentials)
