from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.middleware.role_verification import role_verification_middleware
from src.api.components.ingredients.schemas import IngredientReq, IngredientUpdateReq, Ingredient
from src.api.components.ingredients.service import IngredientsService
from src.db.models import UserRole
from src.api.components.users.controller import oauth2_scheme
from src.middleware.role_auth import roles_required
from src.utils.jwt import verify_token


ADMIN, USER = UserRole.admin, UserRole.user

ingredients_router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"]
)
ingredient_service = IngredientsService()

@ingredients_router.get("/", response_model=list[Ingredient])
async def get_all_ingredients(token: str = Depends(oauth2_scheme)) -> []:
    roles_required([ADMIN, USER], token)
    user_id = verify_token(token)["user_id"]
    try:
        return ingredient_service.get_all_ingredients(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting all ingredients in controller: {e}")
    
@ingredients_router.post("/")
async def create_ingredient(ingredient_req : IngredientReq, token: str = Depends(oauth2_scheme)):
    roles_required([ADMIN, USER], token)
    user_id:str = verify_token(token)["user_id"]
    try:
        json_message = ingredient_service.create_ingredient(ingredient_req, user_id)
        return JSONResponse(status_code=200, content=json_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating ingredient in controller: {e}")

@ingredients_router.put("/{data}")
async def update_ingredient(updates: IngredientUpdateReq, token: str = Depends(oauth2_scheme)):
    roles_required([ADMIN, USER], token)
    try:
        user_id: str = verify_token(token)["user_id"]
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Error finding user: {e}")
    json_message = ingredient_service.update_ingredient(updates, user_id)
    return JSONResponse(status_code=200, content=json_message)


@ingredients_router.delete("/")
async def delete_ingredient(ingredient_id:str):
    try:
        return ingredient_service.delete_ingredient(ingredient_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating ingredient in controller: {e}")
