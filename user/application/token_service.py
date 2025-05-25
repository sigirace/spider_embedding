from fastapi import HTTPException, status
from user.domain.user import User
from utils.jwt import (
    decode_token,
)


class TokenService:

    def validate_token(self, access_token: str) -> User:
        try:
            decoded = decode_token(access_token)

            if "user_id" not in decoded:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload",
                )

            return User(**decoded)

        except Exception:
            raise
