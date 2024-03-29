from fastapi import HTTPException
from fastapi.responses import JSONResponse
from typing import Dict

from src.db.models import Ingredient

class IngredientsRepository:

    def __init__(self, session):
        self.sess = session
    
    def get_all_ingredients(self, user_id):
        try:
            return self.sess.query(Ingredient).filter(Ingredient.user_id == user_id).all()
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Not ingredients found: {e}")
        
    def get_ingredient_by_name(self, ingredient_name: str):
        return self.sess.query(Ingredient).filter(Ingredient.ingredient_name==ingredient_name).first()
    
    def get_ingredient_by_id(self, ingredient_id: str):
        try:
            return self.sess.query(Ingredient).filter(Ingredient.ingredient_id==ingredient_id).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error getting ingredient by id in repository: {e}")

    def create_ingredient(self, new_ingredient):
        try:
            self.sess.add(new_ingredient)
            self.sess.commit()           
            return {"message": f"Ingredient '{new_ingredient.ingredient_name}' created successfully"}
        except Exception as err:
            self.sess.rollback()
            raise HTTPException(status_code=500, detail=f'Could not create ingredient "{new_ingredient.ingredient_name}": {err}')
    
    def update_ingredient(self, id:str, updates):
        print(updates)
        to_update = self.sess.query(Ingredient).filter(Ingredient.ingredient_id == id).first()
        if not to_update:
            raise HTTPException(status_code=404, detail=f"Ingredient not found in repository")
        try:
            self.sess.query(Ingredient).filter(Ingredient.ingredient_id == id).update(updates)
            self.sess.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Couldn't update ingredient: {e}")
        return JSONResponse(status_code=200, content=f"Ingredient {updates['ingredient_name']} updated successfully")

    def delete_ingredient(self, id):
        to_delete = self.sess.query(Ingredient).filter(Ingredient.ingredient_id==id).first()
        if not to_delete:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        try:
            self.sess.delete(to_delete)
            self.sess.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Couldn't delete ingredient: {e}")