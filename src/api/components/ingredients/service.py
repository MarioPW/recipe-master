from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.db.database import session
from src.db.models import User
from src.api.components.users.repository import UserRepository
from src.db.models import Ingredient
from src.api.components.ingredients.repository import IngredientsRepository
from src.api.components.ingredients.schemas import IngredientReq, IngredientUpdateReq

ingredients_repository = IngredientsRepository(session)
user_repository = UserRepository(session)

class IngredientsService(IngredientsRepository):
    def __init__(self) -> None:
        self.ingredients_repository = IngredientsRepository(session)
    
    def get_all_ingredients(self, user_id):
        return ingredients_repository.get_all_ingredients(user_id)
    
    def get_ingredient_by_id(self, id: str):
        try:
            return ingredients_repository.get_ingredient_by_id(id)
        except:
            raise HTTPException(status_code=400, detail="Ingredient not found")

    def create_ingredient(self, ingredient_req:IngredientReq, user_id):
        user_exists: User = user_repository.get_user_by_id(user_id)
        if not user_exists:
            raise HTTPException(status_code=404, detail="User not found")       
        try:
            new_ingredient = Ingredient(
            user_id = user_id,
            ingredient_name = ingredient_req.ingredient_name,
            cost_per_kg = ingredient_req.cost_per_kg,
            has_gluten = ingredient_req.has_gluten ,
            is_vegan = ingredient_req.is_vegan,
            supplier = ingredient_req.supplier,
            brand = ingredient_req.brand
            )
            return self.ingredients_repository.create_ingredient(new_ingredient)
        except Exception as error:
            raise HTTPException(status_code=500, detail=f"Error creating ingerdient in /ingredients/service: {error}")
        
    
    def update_ingredient(self, updates: IngredientUpdateReq, user_id):
      
        ingredient = self.ingredients_repository.get_ingredient_by_id(updates.ingredient_id)
        if not ingredient:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        updates_dict = vars(updates)
        ingredient_dict = vars(ingredient)
        ingredient_dict.pop('_sa_instance_state')
        for i in updates_dict.items():
            if i[1] is not None:
                ingredient_dict[i[0]] = i[1]
        
        self.ingredients_repository.update_ingredient(user_id, ingredient_dict)
        #return JSONResponse(status_code=200, content="Ingredient updated successfully")

    def delete_ingredient(ingredient_id:str):
        to_delete: Ingredient = ingredients_repository.get_ingredient_by_id(ingredient_id)
        if not to_delete:
            raise HTTPException(status_code=404, detail=f"Ingredient not found")
        try:
            ingredients_repository.delete_ingredient(ingredient_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error deleting ingredient {to_delete.ingredient_name}: {e}")
        