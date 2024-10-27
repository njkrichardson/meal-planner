from pathlib import Path
from typing import Optional, Sequence 

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, Session, relationship, selectinload

import database
from ingredients import Ingredient, recipe_ingredient_association
import utils

class Recipe(database.StorageBase): 
    """Base recipe table mapped dataclass. 

    Members 
    -------
    name: Mapped[str] 
        String name of the recipe. 
    """
    __tablename__: str = "recipes"
    name: Mapped[str] = mapped_column(sqlalchemy.String, primary_key=True)
    ingredients: Mapped[list[Ingredient]] = relationship(
        "Ingredient", secondary=recipe_ingredient_association, back_populates="recipes"
    )

Ingredient.recipes = relationship(
    "Recipe", secondary=recipe_ingredient_association, back_populates="ingredients", lazy="joined"
)

class RecipeDatabase: 
    """Recipe database interface class, which essentially wraps a sql database and 
    exposes a basic public API to read and write from the database. 

    Methods 
    -------
    write(recipe: Recipe) -> None:
        Writes the provided recipe to the database. 
    read_all() -> Sequence[Recipe]: 
        Convenience method to read all recipes from the database. 
    read(name: str) -> Sequence[Recipe]: 
        Read from the recipe database using the recipe name. 
    """
    storage_location: Path = utils.DATA_DIRECTORY / "recipes.db"

    def __init__(self, debug: Optional[bool]=False, verbose: Optional[bool]=False): 
        if debug: 
            self.engine = sqlalchemy.create_engine("sqlite+pysqlite:///:memory:", echo=verbose)
        else: 
            self.engine = sqlalchemy.create_engine(f"sqlite+pysqlite:///{str(self.storage_location.absolute())}", echo=verbose)

        database.StorageBase.metadata.create_all(self.engine)

    def write(self, recipe: Recipe) -> None: 
        with Session(self.engine) as session: 
            session.add(recipe)
            session.commit()

    def read_all(self) -> Sequence[Recipe]: 
        with Session(self.engine) as session: 
            return session.execute(sqlalchemy.select(Recipe).order_by(Recipe.name).options(selectinload(Recipe.ingredients))).all()

    def read(self, name: str) -> Sequence[Recipe]: 
        with Session(self.engine) as session: 
            recipe = session.execute(sqlalchemy.select(Recipe).where(Recipe.name == name)).scalar_one_or_none()
            if recipe: 
                ingredients = recipe.ingredients
        return recipe