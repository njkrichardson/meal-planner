from typing import Optional, Sequence 

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, Session

import database

class Recipe(database.StorageBase): 
    """Base recipe table mapped dataclass. 

    Members 
    -------
    name: Mapped[str] 
        String name of the recipe. 
    """
    __tablename__: str = "recipes"
    name: Mapped[str] = mapped_column(primary_key=True)

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
    def __init__(self, in_memory: Optional[bool]=True, debug: Optional[bool]=False): 
        if in_memory: 
            self.engine = sqlalchemy.create_engine("sqlite+pysqlite:///:memory:", echo=debug)
        else: 
            raise NotImplementedError(f"Persistent storage not implemented")

        database.StorageBase.metadata.create_all(self.engine)

    def write(self, recipe: Recipe) -> None: 
        with Session(self.engine) as session: 
            session.add(recipe)
            session.commit()

    def read_all(self) -> Sequence[Recipe]: 
        with Session(self.engine) as session: 
            return session.execute(sqlalchemy.select(Recipe).order_by(Recipe.name)).all()

    def read(self, name: str) -> Sequence[Recipe]: 
        with Session(self.engine) as session: 
            result = session.execute(sqlalchemy.select(Recipe).where(Recipe.name == name))
            return result.all()