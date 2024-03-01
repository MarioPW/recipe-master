
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from src.middleware.role_auth import roles_required
from src.db.models import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")
ADMIN, USER, UNCONFIRMED = UserRole.admin, UserRole.user, UserRole.unconfirmed

async def role_ADMIN(roles: list[UserRole], token: str = Depends(oauth2_scheme)):
    return roles_required(roles, token)

async def role_ADMIN_UNCONFIRMED(token: str = Depends(oauth2_scheme)):
    return roles_required([ADMIN, UNCONFIRMED], token)

async def role_ADMIN_USER(token: str = Depends(oauth2_scheme)):
    return roles_required([ADMIN, USER], token)
