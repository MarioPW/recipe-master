from src.api.components.recipes.repository import RecipeRepository
from src.db.models import session


class RecipeService(RecipeRepository):
    def __init__(self):
        self.recipe_repository = RecipeRepository(session)

    def get_all_recipes(self):
        return "recipes"
    
    def get_recipe_by_id(self, recipe_id):   
        return f"recipe {recipe_id}"
    
    def create_recipe(recipe:RecipeRepository):
        return recipe
    
    def update_recipe(recipe_updates):
        return f"Updates: {recipe_updates}"
    
    def delete_recipe(user_id, recipe_id):
        return f"Delete: {recipe_id}"