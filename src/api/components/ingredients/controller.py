from fastapi import APIRouter, Depends
from src.api.components.ingredients.schemas import IngredientReq, IngredientUpdateReq, Ingredient
from src.api.components.ingredients.service import IngredientsService
from src.db.models import UserRole
from src.api.components.users.controller import oauth2_scheme
from src.middleware.role_auth import roles_required, roles_required_returninig_user_data

#--- Token and user role verification dependency: ---------------------

ADMIN, USER = UserRole.admin, UserRole.user

async def only_admin_or_user_role(token: str = Depends(oauth2_scheme)):
    return roles_required_returninig_user_data([ADMIN, USER], token)

# ---------------------------------------------------------------------

ingredients_router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"],
    dependencies=[Depends(only_admin_or_user_role)]
)
ingredient_service = IngredientsService()

@ingredients_router.get("/", response_model=list[Ingredient])
async def get_all_ingredients(user = Depends(only_admin_or_user_role)) -> []:
    return ingredient_service.get_all_ingredients(user.user_id)

@ingredients_router.get("/{id}")
async def get_ingredient_by_id(id: str, user = Depends(only_admin_or_user_role)):
    return ingredient_service.get_ingredient_by_id(id)
 
@ingredients_router.post("/")
async def create_ingredient(ingredient_req : IngredientReq, user = Depends(only_admin_or_user_role)):  
    return ingredient_service.create_ingredient(ingredient_req, user.user_id)

@ingredients_router.put("/{data}")
async def update_ingredient(updates: IngredientUpdateReq, ingredient_id, user = Depends(only_admin_or_user_role)):
    return ingredient_service.update_ingredient(updates, ingredient_id, user.user_id)

@ingredients_router.delete("/{id}")
async def delete_ingredient(id: str, token: str = Depends(oauth2_scheme)):
    roles_required([ADMIN, USER], token)
    return ingredient_service.delete_ingredient(id)

