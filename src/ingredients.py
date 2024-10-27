from typing import Optional

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column

import database 

recipe_ingredient_association = sqlalchemy.Table(
    "recipe_ingredient", database.StorageBase.metadata,
    sqlalchemy.Column("recipe_name", sqlalchemy.ForeignKey("recipes.name"), primary_key=True),
    sqlalchemy.Column("ingredient_name", sqlalchemy.ForeignKey("ingredients.name"), primary_key=True)
)

class Ingredient(database.StorageBase):
    """Ingredient table with unique ID and name.
    """
    __tablename__ = "ingredients"
    name: Mapped[str] = mapped_column(sqlalchemy.String, primary_key=True, nullable=False, unique=True)
