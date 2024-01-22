from fastapi import APIRouter, HTTPException,  Depends, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import EmailStr
from src.api.components.users.service import UserService
from src.api.components.users.schemas import User, UserRegister, UserUpdateReq, ConfirmationCode
from src.middleware.role_auth import roles_required
from src.db.models import UserRole
from src.utils.jwt import verify_token

users_router = APIRouter(
    prefix="/users",
    tags=["Users"])

user_service = UserService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")
ADMIN, USER, UNCONFIRMED = UserRole.admin, UserRole.user, UserRole.unconfirmed

# Private Routes
@users_router.get("/", response_model=list[User])
async def get_all_users(token: str = Depends(oauth2_scheme)) -> []:
    roles_required([ADMIN], token)
    users:[] = await user_service.get_all_users()
    if not users:
        raise HTTPException(status_code=500, detail="Error getting all users in controller")
    return users

@users_router.get("/user_id/{user_id}", response_model=User)
async def get_user_by_id(user_id: str, token: str = Depends(oauth2_scheme)):
    roles_required([ADMIN], token)
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=500, detail="Error getting user by id incontroller")
    return user

@users_router.get("/email/{user_email}", response_model=User)
async def get_user_by_email(user_email: EmailStr, token: str = Depends(oauth2_scheme)):   
    roles_required([ADMIN], token)
    user = await user_service.get_user_by_email(user_email)
    if not user:
        raise HTTPException(status_code=500, detail="Error getting user by email incontroller")
    return user
    
# Public Routes
@users_router.post("/register_submission")
async def create_register_submition(data: UserRegister):
    try:   
        return await user_service.create_register_submition(data)                
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Opss Couldn't send email to {data.email} in controller: {e}")
    
@users_router.post("/register")
async def create_user(confirmation_code: ConfirmationCode):
    roles_required([ADMIN, UNCONFIRMED], code=confirmation_code)
    try:
        return await user_service.create_user(confirmation_code)
    except Exception:
        raise HTTPException(status_code=422, detail="Error creating user in controller")

@users_router.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    try:
        return await user_service.login(data)
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Login error in controller:{error}")

@users_router.get("/user_main_page")
async def user_main_page(token: str = Header(..., description="Auth token")):
    roles_required([ADMIN, USER], token)
    try:
        return await user_service.user_main_page(token)
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error getting user:{error}")

@users_router.put("/{updates}")
async def update_user(user_updates: UserUpdateReq, token: str = Depends(oauth2_scheme)):
    roles_required([ADMIN, USER], token)
    user_id: str = verify_token(token)["user_id"]
    try:
        update_user = await user_service.update_user(user_id, user_updates)
        if not update_user:
            raise HTTPException(status_code=404, detail="User not found")
        return update_user
              
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Something went wrong in controller:{error}")

@users_router.delete("/{user_id}")
async def delete_user(user_id: str, token: str = Depends(oauth2_scheme)):
    roles_required([ADMIN, USER], token)
    return await user_service.delete_user(user_id)