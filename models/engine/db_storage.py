"""
    This class defines DatabaseStorage.
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """
    New engine DBStorage

    Attributes:
        __engine: SQLAlchemy engine
        __session: SQLAlchemy session
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Create engine and link to MySQL database.
        """
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST", default="localhost"),
                getenv("HBNB_MYSQL_DB"),
            ),
            pool_pre_ping=True,
        )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on the current database session.

        Args:
            cls: Class name (optional). If provided, filters objects by class.

        Returns:
            dict: Dictionary containing queried objects.
        """
        db_dict = {}
        if cls is not None:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                db_dict[key] = obj
        else:
            for cl in [User, State, City, Amenity, Place, Review]:
                objs = self.__session.query(cl).all()
                for obj in objs:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    db_dict[key] = obj
        return db_dict

    def new(self, obj):
        """
        Add the object to the current database session.

        Args:
            obj: The object to be added.
        """
        if obj:
            self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from the current database session.

        Args:
            obj: The object to be deleted. If None, no action is taken.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the database and initialize a new session.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Close the current session.
        """
        self.__session.close()
