#!/usr/bin/python3
"""
Module defines a database engine
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base, BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """
        sets database attribute
    """
    __engine = None
    __session = None

    def __init__(self):
        """
            set username and password
        """
        username = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')

        db_url = "mysql+mysqldb://{}:{}@{}/{}".format(username,
                                                     password,
                                                     host, db)
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadate.drop_all(self.__engine)

    def all(self, cls=None):
        """
            Return a dictionary of class object
        """
        list_object = []
        if cls:
            if isinstance(cls, str):
                try:
                    cls = globals()[cls]
                except KeyError:
                    pass
            if issubclass(cls, Base):
                list_object = self.__session.query(cls).all()
        else:
            for sub_class in Base.__subclasses__():
                list_object.extend(self.__session.query(sub_class).all())
        dict_obj = {}
        for obj in list_object:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            try:
                del obj._sa_instance_state
                dict_obj[key] = obj
            except Exception:
                pass
        return dict_obj

    def new(self, obj):
        """
            Add the new object to the given database
        """
        self.__session.add(obj)

    def save(self):
        """
            save changes to the current session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
            Delete the given object of the current session
        """
        self.__session.delete(obj)

    def reload(self):
        """
        """
        Base.metadata.create_all(self.__engine)
        db_session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(db_session)
        self.__session = Session()
