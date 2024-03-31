#!/usr/bin/python3
"""Defines a base class for all models in the hbnb clone."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()


class BaseModel:
    """Base class for all hbnb models."""
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiates a new model."""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            models.storage.new(self)
        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance."""
        cls = str(type(self)).split('.')[-1].split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with the current time when the instance is changed."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns dictionary representation of instance."""
        dictionary = self.__dict__.copy()

        if "created_at" in dictionary and isinstance(dictionary["created_at"], datetime):
            dictionary["created_at"] = dictionary["created_at"].isoformat()
        if "updated_at" in dictionary and isinstance(dictionary["updated_at"], datetime):
            dictionary["updated_at"] = dictionary["updated_at"].isoformat()
        dictionary["__class__"] = self.__class__.__name__
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """Deletes the current instance from models.storage."""
        models.storage.delete(self)
        models.storage.save()
