from fastapi import APIRouter, Depends
from src.api.components.ingredients.schemas import IngredientReq, IngredientUpdateReq, Ingredient
from src.api.components.ingredients.service import IngredientsService
from src.db.models import UserRole
from src.api.components.users.controller import oauth2_scheme
from src.middleware.role_auth import roles_required

#--- Token and user role verification dependency: ---------------------

ADMIN, USER = UserRole.admin, UserRole.user

def only_ADMIN_or_USER_role(token: str = Depends(oauth2_scheme)):
    return roles_required([ADMIN, USER], token)

# ---------------------------------------------------------------------

ingredients_router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"],
    dependencies=[Depends(only_ADMIN_or_USER_role)]
)
ingredient_service = IngredientsService()

@ingredients_router.get("/{user_id}", response_model=list[Ingredient])
def get_all_ingredients(user_id) -> list:
    return ingredient_service.get_all_ingredients(user_id)

@ingredients_router.get("/{id}")
def get_ingredient_by_id(id: str):
    return ingredient_service.get_ingredient_by_id(id)
 
@ingredients_router.post("/{user_id}")
def create_ingredient(ingredient_req: IngredientReq, user_id):
    return ingredient_service.create_ingredient(ingredient_req, user_id)

@ingredients_router.put("/")
def update_ingredient(updates: IngredientUpdateReq):
    return ingredient_service.update_ingredient(updates)

@ingredients_router.delete("/{id}")
def delete_ingredient(id: str, token: str = Depends(oauth2_scheme)):
    roles_required([ADMIN, USER], token)
    return ingredient_service.delete_ingredient(id)

