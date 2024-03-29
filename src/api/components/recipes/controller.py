from fastapi import APIRouter, HTTPException, Depends
from src.db.models import UserRole
from src.middleware.role_auth import roles_required, verify_token, roles_required_returninig_user_data
from src.api.components.users.controller import oauth2_scheme
from src.api.components.recipes.service import RecipeService

recipes_router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)
ADMIN, USER, UNCONFIRMED = UserRole.admin, UserRole.user, UserRole.unconfirmed

#--- Token and user role verification dependency: ---------------------

ADMIN, USER = UserRole.admin, UserRole.user

def only_ADMIN_or_USER_role(token: str = Depends(oauth2_scheme)):
    return roles_required_returninig_user_data([ADMIN, USER], token)

# ---------------------------------------------------------------------

recipe_service = RecipeService()


@recipes_router.get("/")
def my_recipes(user = Depends(only_ADMIN_or_USER_role)):  
    return recipe_service.get_all_recipes(user.user_id)

@recipes_router.post("/")
def create_recipe(token: str = Depends(oauth2_scheme)):
    if not roles_required([ADMIN, USER], token):
        raise HTTPException(status_code=403, detail="Access denied")
    return verify_token(token)