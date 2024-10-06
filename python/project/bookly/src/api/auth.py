from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from fastapi import Request, status
from abc import abstractmethod, ABC 
from src.utils.security import decode_token


class TokenBearer(HTTPBearer, ABC):
    """Authorization"""
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        _, credentials = creds.scheme, creds.credentials
        is_valid, token_data = self.token_valid(credentials)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token"
            )
        self.verify_token_data(token_data)
        
        return creds

    def token_valid(self, token: str) -> tuple[bool, dict]:
        token_data = decode_token(token)
        is_valid = True if token_data else False
        return is_valid, token_data

    @abstractmethod
    def verify_token_data(self, token_data):
        """Verify if the token is for valid method"""



class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide Access Token",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide Refresh Token",
            )
