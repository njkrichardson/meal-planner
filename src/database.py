from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

class StorageBase(MappedAsDataclass, DeclarativeBase): 
    pass 