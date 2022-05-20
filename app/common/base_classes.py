from typing import Optional

from fastapi import HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param


class OAuth2PasswordBearerHeader(OAuth2PasswordBearer):

    async def __call__(self, authorization: str | None = Header(...)) -> Optional[str]:
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param
