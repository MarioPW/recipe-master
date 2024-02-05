from fastapi import APIRouter, HTTPException, Depends
from src.db.models import UserRole
from src.middleware.role_auth import roles_required, verify_token
from src.api.components.users.controller import oauth2_scheme

recipes_router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)
ADMIN, USER, UNCONFIRMED = UserRole.admin, UserRole.user, UserRole.unconfirmed


@recipes_router.get("/")
async def my_recipes(token: str = Depends(oauth2_scheme)):  
    if not roles_required([ADMIN, USER], token):
        raise HTTPException(status_code=403, detail="Access denied")
    return "panes"

@recipes_router.post("/")
async def create_recipe(token: str = Depends(oauth2_scheme)):
    if not roles_required([ADMIN, USER], token):
        raise HTTPException(status_code=403, detail="Access denied")
    return verify_token(token)