from enum import Enum as pyEnum

class UserRole(str, pyEnum):
    user = "5cfbe49a-c985-4d11-94f7-7a7240f1ad35"
    admin = "5d75f0e3-394e-466b-9f74-e2f2c1f1fd4d"
    deleted = "aa9b1d4a-1c4d-4e67-ad2c-dbf36bdf1b8e"
    guest = "e0c33d6b-f2f4-4cc2-b907-1bb083c6af7b"
    unconfirmed = "7b11fd10-c30e-4122-8735-3d95f98f4ee7"

class Unit_of_meassure(pyEnum):
    KILOGRAM = "kg"
    GRAM = "g"
    POUND = "lb"
    OUNCE = "oz"
    LITER = "L"
    MILLILITER = "ml"
    GALLON = "gal"
    FLUID_OUNCE = "fl_oz"