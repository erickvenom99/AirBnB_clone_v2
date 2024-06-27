#!/usr/bin/python3
"""
This module defines a class to manage file storage for hbnb clone.
"""
import json
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class FileStorage:
    """
    This class manages storage of hbnb models in JSON format.
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Retrieves all objects of a specific class from __objects.

        Args:
            cls (type): Class to filter objects by.

        Returns:
            dict: A dictionary containing matching objects
                (key: object ID, value: object).
            If cls is not provided or doesn't meet the conditions,
                 returns all objects.
        """
        if cls:
            if isinstance(cls, str):
                cls = globals().get(cls)
            if cls and issubclass(cls, BaseModel):
                cls_dict = {k: v for k,
                            v in self.__objects.items() if isinstance(v, cls)}
                return cls_dict
        return FileStorage.__objects

    def new(self, obj):
        """Adds a new object to the storage dict
        3ionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def delete(self, obj=None):
        """Deletes an object from the __objects dictionary if it's inside"""
        if obj is None:
            return
        key_del = "{}.{}".format(obj.__class__.__name__, obj.id)
        try:
            del FileStorage.__objects[key_del]
        except (KeyboardInterrupt, AttributeError):
            pass

    def save(self):
        """Saves the storage dictionary to a file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads the storage dictionary from a file"""
        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass
