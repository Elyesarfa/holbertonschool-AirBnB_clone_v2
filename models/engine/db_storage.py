#!/usr/bin/python3
"""
DBStorage class module for SQLAlchemy storage engine in AirBnB Clone.
"""

from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

class DBStorage():
    """
    SQLAlchemy storage engine for AirBnB Clone.

    Attributes:
    __engine (sqlalchemy.Engine): SQLAlchemy engine.
    __session (sqlalchemy.Session): SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initializes DBStorage instance."""
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"),
                getenv("HBNB_MYSQL_DB")
            ),
            pool_pre_ping=True
        )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Retrieves objects from database."""
        if cls is not None:
            if isinstance(cls, str):
                cls = eval(cls)
            objects = self.__session.query(cls)
        else:
            objects = self.__session.query(State).all() + \
                self.__session.query(City).all() + \
                self.__session.query(User).all() + \
                self.__session.query(Place).all() + \
                self.__session.query(Review).all() + \
                self.__session.query(Amenity).all()
        return {
            "{}.{}".format(type(obj).__name__, obj.id): obj for obj in objects
        }

    def new(self, obj):
        """Adds new object to database session."""
        self.__session.add(obj)

    def save(self):
        """Commits changes to database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes object from database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates tables in database and starts new session."""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """Closes SQLAlchemy session."""
        self.__session.close()
