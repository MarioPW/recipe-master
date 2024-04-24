from pydantic import BaseModel, model_validator
from src.db.enums import Unit_of_measure


class Recipe(BaseModel):
    ingredient_id: str
    user_id: str
    ingredient_name: str
    cost: float
    unit_of_measure: str
    has_gluten: bool
    is_vegan: bool
    supplier: str
    brand: str

class Recipe_req:
    recipe_name: str
    weight_per_unit: float
    unit_of_measure: Unit_of_measure
    category: str
    @model_validator(mode='after')
    def check_unit_of_measure(self):
        if self.unit_of_measure in Unit_of_measure:
            self.unit_of_measure = self.unit_of_measure.value
            return self