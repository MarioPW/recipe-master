from fastapi import APIRouter, HTTPException,  Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import EmailStr
from src.api.components.users.service import UserService
from src.api.components.users.schemas import User, UserRegister, UserUpdateReq, ConfirmationCode
from src.middleware.role_auth import roles_required
from src.db.models import UserRole
from src.utils.jwt_handler import verify_token

users_router = APIRouter(
    prefix="/users",
    tags=["Users"])

user_service = UserService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")
ADMIN, USER, UNCONFIRMED = UserRole.admin, UserRole.user, UserRole.unconfirmed

@users_router.get("/", response_model=list[User])
def get_all_users(token: str = Depends(oauth2_scheme)) -> []:
    roles_required([ADMIN], token)
    return user_service.get_all_users()

@users_router.get("/user_id/{user_id}", response_model=User)
def get_user_by_id(user_id: str, token: str = Depends(oauth2_scheme)):
    roles_required([ADMIN], token)
    return user_service.get_user_by_id(user_id)

@users_router.get("/email/{user_email}", response_model=User)
def get_user_by_email(user_email: EmailStr, token: str = Depends(oauth2_scheme)):   
    roles_required([ADMIN], token)
    return user_service.get_user_by_email(user_email)

@users_router.post("/register_submission")
def create_register_submition(data: UserRegister):
    return user_service.create_register_submition(data)                
    
@users_router.post("/confirm_user")
def confirm_user(confirmation_code: ConfirmationCode):
    roles_required([ADMIN, UNCONFIRMED], code=confirmation_code)
    return user_service.confirm_user(confirmation_code)

@users_router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    return user_service.login(data)

@users_router.put("/{updates}")
def update_user(user_updates: UserUpdateReq, token: str = Depends(oauth2_scheme)):
    roles_required([ADMIN, USER], token)
    user_id: str = verify_token(token)["user_id"]
    return user_service.update_user(user_id, user_updates)

@users_router.delete("/{user_id}")
def delete_user(user_id: str, token: str = Depends(oauth2_scheme)):
    roles_required([ADMIN, USER], token)
    return user_service.delete_user(user_id)

@users_router.post("/forgot_password/{email}")
def forgot_password(email: EmailStr):
    return user_service.forgot_password(email)

@users_router.post("/update_password/{data}")
def update_password(email: EmailStr):
    return user_service.forgot_password(email)