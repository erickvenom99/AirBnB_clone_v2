#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from sqlalchemy import (Column, String,
                        Integer, Float,
                        ForeignKey, Table)
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models
from models.review import Review
from models.amenity import Amenity

linke_table = Table('place_amenity', Base.metadata, 
                    Column('place_id', String(60), ForeignKey('place.id'),
                    primary_key=True, nullable=False),
                    Column('amenity_id', String(60), ForeignKey('amenities.id'),
                    primary_key=True, nullable=False))

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    review = relationship('Review', backref='place', cascade='all, delete-orphan')
    amenities = relationship('Amenity', secondary='place_amenity', viewonly=False)
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def review(self):
            """Return list of reviews"""
            rel_review = list(models.storage.all(Review).values())
            list_re = [r for r in rel_review if r.place_id == self.id]
            return list_re
        
        @property
        def amenities(self):
            """
            """
            list_amenity = list(models.storage.all(Amenity).values())
            all_amenity = [a for a in list_amenity if a.id in self.amenity_ids]
            return all_amenity
        
        @amenities.setter
        def amenities(self, value):
            """
            """
            if isinstance(value, Amenity):
                self.amenity_ids.append(value.id)        