from fastapi import HTTPException

from src.db.models import Recipe

class RecipeRepository():
    def __init__(self, session):
        self.sess = session

    def get_all_recipes(self, user_id):
        try:
            return self.sess.query(Recipe).filter(Recipe.user_id == user_id).all()
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Not recipes found: {e}")