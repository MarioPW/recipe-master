
#### THIS SCRIPT CAN BE EXECUTEd TO CREATE DATABASE TABLES AND RELATIONSHIPS ####

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as pyEnum
from sqlalchemy.types import Enum
from src.db.database import Base, engine

class UserRole(str, pyEnum):
    user = "5cfbe49a-c985-4d11-94f7-7a7240f1ad35"
    admin = "5d75f0e3-394e-466b-9f74-e2f2c1f1fd4d"
    deleted = "aa9b1d4a-1c4d-4e67-ad2c-dbf36bdf1b8e"
    guest = "e0c33d6b-f2f4-4cc2-b907-1bb083c6af7b"
    unconfirmed = "7b11fd10-c30e-4122-8735-3d95f98f4ee7"

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
    recipe_name = Column(String, nullable=False)
    unit_weight = Column(Integer, default=0)

    user = relationship('User', back_populates='recipes')
    ingredients = relationship('IngredientRecipe', back_populates='recipe')

class Ingredient(Base):
    __tablename__ = 'ingredients'
    ingredient_id = Column(Integer, autoincrement="auto", primary_key=True, unique=True)
    user_id = Column(String, ForeignKey('users.user_id'))
    ingredient_name = Column(String, nullable=False)
    cost_per_kg = Column(Float, nullable=False, default=0)
    has_gluten = Column(Boolean, nullable=False, default=False)
    is_vegan = Column(Boolean, nullable=False, default=False)
    supplier = Column(String, nullable=False, default="No defined supplier")
    brand = Column(String, nullable=False, default="No defined brand")
       
    recipes = relationship('IngredientRecipe', back_populates='ingredient')
    user = relationship('User', back_populates='ingredients')
    __table_args__ = (UniqueConstraint('user_id', 'ingredient_name', name='uq_user_ingredient_name'),)

class IngredientRecipe(Base):
    __tablename__ = 'ingredients_recipes'
    ingredient_recipe_id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'))
    ingredient_id = Column(Integer, ForeignKey('ingredients.ingredient_id'))
    weight = Column(Integer, nullable=False)

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

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)