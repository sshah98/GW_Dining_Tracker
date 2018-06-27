# -*- coding: utf-8 -*-

import sys
import os
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Binary
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(SQLALCHEMY_DATABASE_URI)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(), unique=True)
    password = Column(Binary())
    email = Column(String(), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username


class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    account = Column(String())
    time = Column(DateTime)
    vendor = Column(String())
    price = Column(Float)
    email = Column(String(), ForeignKey('users.email'))
    datetime = Column(DateTime)

    def __repr__(self):
        return '<id {}>'.format(self.id)


engine = db_connect()  # Connect to database
Base.metadata.create_all(engine)  # Create models
