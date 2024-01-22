from pydantic import BaseModel

class Ingredient(BaseModel):
    ingredient_id: int
    user_id: str
    ingredient_name: str
    cost_per_kg: float
    has_gluten: bool
    is_vegan: bool
    supplier: str
    brand: str

class IngredientReq(BaseModel):
    ingredient_name: str
    cost_per_kg: float
    has_gluten: bool 
    is_vegan: bool
    supplier: str
    brand: str

class IngredientUpdateReq(BaseModel):
    ingredient_id:int
    ingredient_name: str = None
    cost_per_kg: float = None
    has_gluten: bool = None
    is_vegan: bool = None
    supplier: str = None
    brand: str = None