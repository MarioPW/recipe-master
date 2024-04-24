# from fastapi import APIRouter, HTTPException, Depends
# from src.db.models import UserRole
# from src.middleware.role_auth import roles_required, verify_token, roles_required_returninig_user_data
# from src.api.components.users.controller import oauth2_scheme
# from src.api.components.recipes.service import RecipeService
# from .schemas import Recipe_req

# recipes_router = APIRouter(
#     prefix="/recipes",
#     tags=["Recipes"]
# )
# ADMIN, USER, UNCONFIRMED = UserRole.admin, UserRole.user, UserRole.unconfirmed

# #--- Token and user role verification dependency: ---------------------

# ADMIN, USER = UserRole.admin, UserRole.user

# def only_ADMIN_or_USER_role(token: str = Depends(oauth2_scheme)):
#     return roles_required_returninig_user_data([ADMIN, USER], token)

# # ---------------------------------------------------------------------

# recipe_service = RecipeService()


# @recipes_router.get("/")
# def get_all_recipes(user = Depends(only_ADMIN_or_USER_role)):  
#     return recipe_service.get_all_recipes(user.user_id)

# @recipes_router.get("/")
# def get_recipe_by_id(recipe_id, user = Depends(only_ADMIN_or_USER_role)):  
#     return recipe_service.get_recipe_by_id(user.user_id, recipe_id)

# @recipes_router.post("/")
# def create_recipe(recipe: Recipe_req, user = Depends(only_ADMIN_or_USER_role)):
#     if not user:
#         raise HTTPException(status_code=403, detail="Access denied")
#     return recipe_service.create_recipe(user.user_id, recipe)

# @recipes_router.put("/{recipe_id}")
# def update_recipe(recipe_id, token: str = Depends(oauth2_scheme)):
#     if not roles_required([ADMIN, USER], token):
#         raise HTTPException(status_code=403, detail="Access denied")
#     return recipe_service.update_recipe(recipe_id, token)