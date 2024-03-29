from src.api.components.recipes.repository import RecipeRepository
from src.db.database import session


class RecipeService(RecipeRepository):
    def __init__(self):
        self.recipe_repository = RecipeRepository(session)

    def get_all_recipes(self):
        return "recipes"