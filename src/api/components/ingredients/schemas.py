from pydantic import BaseModel
from src.db.models import Unit_of_meassure
class Ingredient(BaseModel):
    ingredient_id: str
    user_id: str
    ingredient_name: str
    cost: float
    unit_of_meassure: Unit_of_meassure
    has_gluten: bool
    is_vegan: bool
    supplier: str
    brand: str

class IngredientReq(BaseModel):
    ingredient_name: str
    cost: float
    unit_of_meassure: Unit_of_meassure
    has_gluten: bool = None
    is_vegan: bool
    supplier: str
    brand: str

class IngredientUpdateReq(BaseModel):
    ingredient_id: str
    ingredient_name: str = None
    cost: float = None
    unit_of_meassure: Unit_of_meassure = None
    has_gluten: bool = None
    is_vegan: bool = None
    supplier: str = None
    brand: str = None