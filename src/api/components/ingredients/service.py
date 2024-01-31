from fastapi import HTTPException
from fastapi.responses import JSONResponse
import uuid
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
        id = str(uuid.uuid4())
        if not user_exists:
            raise HTTPException(status_code=404, detail="User not found")       
        try:
            new_ingredient = Ingredient(
            user_id = id,
            ingredient_name = ingredient_req.ingredient_name,
            cost = ingredient_req.cost,
            unit_of_meassure = ingredient_req.unit_of_meassure,
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

    def delete_ingredient(self, ingredient_id):
        try:
            to_delete: Ingredient = ingredients_repository.get_ingredient_by_id(ingredient_id)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Ingredient not found: {e}")
        ingredients_repository.delete_ingredient(ingredient_id)
        return JSONResponse(status_code=200, content=f'Ingredient "{to_delete.ingredient_name}" deleted successfully.')