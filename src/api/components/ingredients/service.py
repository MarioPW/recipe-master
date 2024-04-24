from fastapi import HTTPException
from fastapi.responses import JSONResponse
import uuid
import json
from src.db.database import session
from src.db.models import User
from src.api.components.users.repository import UserRepository
from src.db.models import Ingredient
from src.api.components.ingredients.repository import IngredientsRepository
from src.api.components.ingredients.schemas import IngredientReq, IngredientUpdateReq


class IngredientsService(IngredientsRepository, UserRepository):
    def __init__(self) -> None:
        self.ingredients_repository = IngredientsRepository(session)
        self.user_repository = UserRepository(session)
    
    def get_all_ingredients(self, user_id):
        return self.ingredients_repository.get_all_ingredients(user_id)
    
    def get_ingredient_by_id(self, id: str):
        return self.ingredients_repository.get_ingredient_by_id(id)

    def create_ingredient(self, ingredient_req, user_id):
        user_exists: User = self.user_repository.get_user_by_id(user_id)
        if not user_exists:
            raise HTTPException(status_code=404, detail="User not found")       
        try:
            new_ingredient = Ingredient(
            ingredient_id = str(uuid.uuid4()),
            user_id = user_id,
            ingredient_name = ingredient_req.ingredient_name,
            cost = ingredient_req.cost,
            unit_of_measure = ingredient_req.unit_of_measure,
            has_gluten = ingredient_req.has_gluten ,
            is_vegan = ingredient_req.is_vegan,
            supplier = ingredient_req.supplier,
            brand = ingredient_req.brand
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error creating ingerdient in .../ingredients/service: {e}")
        return self.ingredients_repository.create_ingredient(new_ingredient)
        
    def update_ingredient(self, updates: IngredientUpdateReq, id):
        ingredient = self.ingredients_repository.get_ingredient_by_id(id)
        if not ingredient:
            raise HTTPException(status_code=404, detail="Ingredient not found in service")  
        updates_dict = updates.model_dump()

        return self.ingredients_repository.update_ingredient(id, updates_dict)

    def delete_ingredient(self, ingredient_id):
        try:
            to_delete: Ingredient = self.ingredients_repository.get_ingredient_by_id(ingredient_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Ingredient not found: {e}")
        self.ingredients_repository.delete_ingredient(ingredient_id)
        return JSONResponse(status_code=200, content=f'Ingredient "{to_delete.ingredient_name}" deleted successfully.')