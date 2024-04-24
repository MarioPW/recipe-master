from fastapi import APIRouter
from src.middleware.role_auth import roles_required
from .components.users.controller import users_router
# from .components.recipes.controller import recipes_router
from .components.ingredients.controller import ingredients_router


router = APIRouter()

router.include_router(users_router)
# router.include_router(recipes_router)
router.include_router(ingredients_router)
