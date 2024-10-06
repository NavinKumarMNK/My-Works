import jwt
import uuid

from passlib.context import CryptContext
from datetime import timedelta, datetime
from src.config.settings import ENV_CONFIG
from src.config.handler import logger

password_context = CryptContext(schemes=["bcrypt"])


def generate_password_hash(password: str) -> str:
    hash_ = password_context.hash(password)
    return hash_


def verify_password(password: str, hash_: str) -> bool:
    is_verified = password_context.verify(password, hash_)
    return is_verified


def create_access_token(
    user_data: dict,
    expiry: timedelta = timedelta(seconds=ENV_CONFIG.JWT_MAXAGE),
    refresh: bool = False
):
    payload = {}

    payload['user'] = user_data
    payload['expiry'] = str(datetime.now() + expiry)
    payload['jti'] = str(uuid.uuid4)
    payload['refresh'] = refresh
    
    print(payload)

    token = jwt.encode(
        payload=payload,
        key=ENV_CONFIG.JWT_SECRET_KEY,
        algorithm=ENV_CONFIG.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=ENV_CONFIG.JWT_SECRET_KEY,
            algorithms=[ENV_CONFIG.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PYJWTError as e:
        logger.error(e)
        return None
