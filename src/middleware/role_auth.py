from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.utils.jwt import verify_token
from src.db.models import UserRole
from src.api.components.users.repository import UserRepository
from src.api.components.users.service import session
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")
ADMIN, USER, UNCONFIRMED = UserRole.admin, UserRole.user, UserRole.unconfirmed

user_repository = UserRepository(session)

def roles_required(allowed_roles:list, token=None, code=None) -> None:
    user = None
    if token:
        decoded_user = verify_token(token)
        if decoded_user:
               user = user_repository.get_user_by_id(decoded_user["user_id"])
    elif code:
        user = user_repository.get_user_by_code(code)    
    if user is None or user.role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Access denied")

def role_admin_middleware(token: str = Depends(oauth2_scheme)):
    has_required_role = roles_required([UserRole.user], token)
    if not has_required_role:
        raise HTTPException(status_code=403, detail="Access denied")