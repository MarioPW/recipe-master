from pydantic import BaseModel, model_validator
class Ingredient(BaseModel):
    ingredient_id: str
    user_id: str
    ingredient_name: str
    cost: float
    unit_of_meassure: str
    has_gluten: bool
    is_vegan: bool
    supplier: str
    brand: str

class IngredientReq(BaseModel):
    ingredient_name: str
    cost: float
    unit_of_meassure: str
    has_gluten: bool
    is_vegan: bool
    supplier: str
    brand: str

    @model_validator(mode='after')
    def check_optional_atributes(self) -> 'IngredientReq':
        pass
        # ToDo: check_optional_atributes...


class IngredientUpdateReq(BaseModel):
    ingredient_name: str = None
    ingredient_id: str
    cost: float = None
    unit_of_meassure: str = None
    has_gluten: bool = None
    is_vegan: bool = None
    supplier: str = None
    brand: str = None
