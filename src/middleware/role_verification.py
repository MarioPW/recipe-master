from fastapi import Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.utils.jwt_handler import verify_token
from src.db.models import UserRole
from src.api.components.users.repository import UserRepository
from src.api.components.users.service import session
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")
ADMIN, USER, UNCONFIRMED = UserRole.admin, UserRole.user, UserRole.unconfirmed

user_repository = UserRepository(session)

async def role_verification_middleware(request: Request, call_next) -> Request:
    allowed_roles = [ADMIN, USER]
    authorization_header = request.headers.get("Authorization")   
    if not authorization_header or not authorization_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or no token given.")
    token = authorization_header.split("Bearer ")[1]
    user = None
    if token:
        decoded_user = verify_token(token)
        if decoded_user:
               user = user_repository.get_user_by_name(decoded_user["name"])      
    if user is None or user.role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Access denied")
    response = await call_next(request)
    return response