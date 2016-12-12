# coding: utf-8
__author__ = 'david'
from operator import attrgetter

from flask.ext.babel import gettext
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from flask_template.logger.log import create_logger, log

logger = create_logger(__name__)
Base = declarative_base()


# UTIL DB METHODS
def init_engine(uri, migrate, **kwargs):
    global engine
    global db_session
    
    engine = create_engine(uri, convert_unicode=True, **kwargs)

    try:
        if migrate:
            Base.metadata.create_all(engine)
    except OperationalError:
        log(logger, 'init', repr(OperationalError))

    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))

    return engine


def get_session():
    return db_session


def close_connection():
    """Close the database connection when at request's end"""

    get_session().remove()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('seq_users'), primary_key=True)
    name = Column(String)
    email = Column(String)
    username = Column(String(12))
    password = Column(String(10))


    def as_dict(self, desired_fields=[]):
        response = {}
        for field in desired_fields:
            field_value = attrgetter(field)(self)
            try:
                response[field] = field_value.get_as_dict()
            except AttributeError:
                response[field] = field_value
        
        return response
        #return {
        #    "id": self.id,
        #    "name": self.name,
        #    "email": self.email,
        #    "username": self.username,
        #    "password": self.password
        #}

    def __repr__(self):
        return ('''User(id=%r, name=%r, email=%r, username=%r, password=%r)''' %
                        (self.id, self.name, self.email, self.username,
                        self.password))
