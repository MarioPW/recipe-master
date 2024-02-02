from enum import Enum as pyEnum

class UserRole(str, pyEnum):
    user = "user"
    admin = "admin"
    deleted = "deleted"
    guest = "guest"
    unconfirmed = "unconfirmed"

class Unit_of_meassure(pyEnum):
    KILOGRAM = "kg"
    GRAM = "g"
    POUND = "lb"
    OUNCE = "oz"
    LITER = "L"
    MILLILITER = "ml"
    GALLON = "gal"
    FLUID_OUNCE = "fl_oz"