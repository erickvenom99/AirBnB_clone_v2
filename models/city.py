#!/usr/bin/python3
""" City Module for HBNB project """
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String
from models.base_model import BaseModel, Base

class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = 'cities'
    name = Column(String(60), nullable=False)
    state_id = Column(String(128), ForeignKey('state.id'), nullable=False)
    places = relationship('Place', backref='cities', cascade='all, delete-orphan')
    
