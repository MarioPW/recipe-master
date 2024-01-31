from fastapi import HTTPException
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

    def create_ingredient(self, new_ingredient: Ingredient):
        try:
            self.sess.add(new_ingredient)
            self.sess.commit()           
            return {"message": f'Ingredient " {new_ingredient.ingredient_name} " created siccessfully'}
        except Exception as err:
            self.sess.rollback()
            raise HTTPException(status_code=500, detail=f"Couldn't create ingredient {new_ingredient.ingredient_name}: {err}")
    
    # def update_ingredient(self, id:str, updates:Dict, user_id:str):
    #     to_update = self.sess.query(Ingredient).filter(Ingredient.ingredient_id == id).update(updates)
    #     if not to_update:
    #         raise HTTPException(status_code=404, detail=f"Ingredient not found")
    #     try:
    #         self.sess.update(to_update)
    #         self.sess.commit()
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f"Couldn't update ingredient: {e}")

    def update_ingredient(self, user_id: str, updates):
        try:
            ingredient = self.sess.query(Ingredient).filter(
                Ingredient.ingredient_id == updates["ingredient_id"],
                Ingredient.user_id == user_id
            ).update(updates)

            if not ingredient:
                raise HTTPException(status_code=404, detail="Ingredient not found or does not belong to the user")

            for key, value in updates.items():
                setattr(ingredient, key, value)
            self.sess.update(ingredient)
            self.sess.commit()
            return {"message": f"Ingredient {ingredient.ingredient_name} updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Couldn't update ingredient in repository: {e}")
        
    def delete_ingredient(self, id):
        to_delete = self.sess.query(Ingredient).filter(Ingredient.ingredient_id==id).first()
        if not to_delete:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        try:
            self.sess.delete(to_delete)
            self.sess.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Couldn't delete ingredient: {e}")