
#### THIS SCRIPT CAN BE EXECUTEd TO CREATE DATABASE TABLES AND RELATIONSHIPS ####

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.types import Enum
from os import getenv
from passlib.context import CryptContext
import uuid

from src.db.database import Base, engine, session
from src.db.enums import UserRole, Unit_of_meassure

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    creation_date = Column(DateTime,default=datetime.now,onupdate=datetime.now)
    role = Column(Enum(UserRole), default=UserRole.unconfirmed)
    confirmation_code = Column(Integer, nullable=False, default=0)
    
    ingredients = relationship('Ingredient', back_populates='user')
    recipes = relationship('Recipe', back_populates='user')
    shared_recipes = relationship('SharedRecipe', back_populates='from_user', foreign_keys='SharedRecipe.from_user_id')

class Recipe(Base):
    __tablename__ = 'recipes'
    recipe_id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.user_id'))
    recipe_name = Column(String, nullable=False, default='Recipe')
    weight_per_unit = Column(Integer, default=0)
    category = Column(String, nullable=False, default='All Recipes')
    user = relationship('User', back_populates='recipes')
    ingredients = relationship('IngredientRecipe', back_populates='recipe')

class Ingredient(Base):
    __tablename__ = 'ingredients'
    ingredient_id = Column(String, primary_key=True, unique=True)
    user_id = Column(String, ForeignKey('users.user_id'))
    ingredient_name = Column(String, nullable=False)
    cost = Column(Float, nullable=False, default=0)
    unit_of_meassure = Column(Enum(Unit_of_meassure), nullable=False)
    has_gluten = Column(Boolean, nullable=False, default=False)
    is_vegan = Column(Boolean, nullable=False, default=False)
    supplier = Column(String, nullable=False, default="Undefined supplier")
    brand = Column(String, nullable=False, default="Undefined brand")
       
    recipes = relationship('IngredientRecipe', back_populates='ingredient')
    user = relationship('User', back_populates='ingredients')
    __table_args__ = (UniqueConstraint('user_id', 'ingredient_name', name='uq_user_ingredient_name'),)

class IngredientRecipe(Base):
    __tablename__ = 'ingredients_recipes'
    ingredient_recipe_id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'))
    ingredient_id = Column(String, ForeignKey('ingredients.ingredient_id'))
    weight = Column(Integer, nullable=False)
    unit_of_meassure = Column(Enum(Unit_of_meassure), nullable=False)

    recipe = relationship('Recipe', back_populates='ingredients')
    ingredient = relationship('Ingredient', back_populates='recipes')

class SharedRecipe(Base):
    __tablename__ = 'shared_recipes'
    share_id = Column(Integer, primary_key=True)
    from_user_id = Column(String, ForeignKey('users.user_id'))
    to_user_id = Column(String, ForeignKey('users.user_id'))
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'))

    from_user = relationship('User', back_populates='shared_recipes', foreign_keys='SharedRecipe.from_user_id')
    to_user = relationship('User', back_populates='shared_recipes', foreign_keys='SharedRecipe.to_user_id')
    recipe = relationship('Recipe')

#### Lookup Tables ####

class UnitOfMeassureLookup(Base):
    __tablename__ = 'Units_of_meassure_lookup'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    unit_of_meassure  = Column(String, unique=True)

class UserRolesLookup(Base):
    __tablename__ = 'User_roles_lookup'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_role = Column(String, unique=True)

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Migrations to database executed correctly.")

#### INSERTION OF ENUMS DATA INTO LOOKUP TABLES:

    for unit in Unit_of_meassure:
        new_unit = UnitOfMeassureLookup(unit_of_meassure=unit.value)
        session.add(new_unit)

    for role in UserRole:
        new_role = UserRolesLookup(user_role=role.name)
        session.add(new_role)

####  INSERTION OF ADMIN USER DATA INTO USERS TABLE:
    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    name = getenv("NAME")
    email = getenv("ADMIN_EMAIL")
    role = UserRole.admin

    admin_user_password = getenv("PASSWORD")
    admin_user_password_hash = bcrypt_context.hash(admin_user_password)
    admin_user = User(user_id = str(uuid.uuid4()), name=name, email=email, password_hash=admin_user_password_hash, role=role)
    
    session.add(admin_user)
    session.commit()
    session.close()