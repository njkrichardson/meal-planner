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

    Members
    -------
    name: str 
        Ingredient name. 
    quantity: int 
        Quantity of ingredient (in grams). 
    """
    __tablename__ = "ingredients"
    name: Mapped[str] = mapped_column(sqlalchemy.String, primary_key=True, nullable=False, unique=True)
    quantity: Mapped[int] = mapped_column(sqlalchemy.Integer, nullable=True)

    def __repr__(self) -> str: 
        return f"{self.__class__.__name__}(name={self.name}, quantity={self.quantity}g)"


