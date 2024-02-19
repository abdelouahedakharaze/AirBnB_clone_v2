#!/usr/bin/python3
"""
Conditional initialization of storage module based on environment variable HBNB_TYPE_STORAGE.
If set to 'db', imports DBStorage class and initializes storage with it.
Otherwise, imports FileStorage class and initializes storage.
Allows dynamic storage type change via HBNB_TYPE_STORAGE.
"""
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.user import User
from models.base_model import BaseModel
from os import getenv

if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage

    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage

    storage = FileStorage()

storage.reload()
