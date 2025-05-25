from fastapi import HTTPException
from config import get_settings
from jose import ExpiredSignatureError, JWTError, jwt

settings = get_settings()

jwt_config = settings.jwt

ALGORITHM = jwt_config.jwt_algorithm
SECRET_KEY = jwt_config.jwt_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = jwt_config.access_token_expires_in
REFRESH_TOKEN_EXPIRES_IN = jwt_config.refresh_token_expires_in


def decode_token(token: str) -> dict:
    try:
        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return decoded

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=440,
            detail="Token has expired",
        )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal error decoding token: {str(e)}",
        )
