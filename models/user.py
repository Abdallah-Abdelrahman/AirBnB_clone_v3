#!/usr/bin/python3
""" holds class User"""
from hashlib import md5
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.db:
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __setattr__(self, name, value):
        '''overload setattr
        Args:
            name: the key
            value: key's value
        '''
        if name == 'password':
            value = md5(value.encode()).hexdigest()

        return super().__setattr__(name, value)
