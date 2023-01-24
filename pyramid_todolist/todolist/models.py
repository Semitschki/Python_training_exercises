''' Contains all database models. '''
from datetime import datetime
from random import choice
import string

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Unicode,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def _generate_token(length):
    ''' Generate and return URL safe token. '''
    alphabet = string.ascii_letters + string.digits
    return ''.join(choice(alphabet) for _ in range(length))


class Task(Base):
    ''' Tasks for the TodoList. '''
    __tablename__ = 'app_task'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    note = Column(Unicode)
    creation_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('app_user.id'), nullable=False)
    user = relationship('User', back_populates='tasks')

    def __init__(self, *args, **kwargs):
        ''' On initialization, set date of creation. '''
        super().__init__(*args, **kwargs)
        self.creation_date = datetime.now()


class User(Base):
    ''' User for the TodoList. '''
    __tablename__ = 'app_user'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode, nullable=False)
    email = Column(Unicode, nullable=False)
    password = Column(Unicode, nullable=False)
    date_joined = Column(DateTime, nullable=False)
    token = Column(Unicode, nullable=False)
    tasks = relationship('Task', back_populates='user')

    def __init__(self, *args, **kwargs):
        ''' On initialization, set date of creation. '''
        super().__init__(*args, **kwargs)
        self.date_joined = datetime.now()
        self.token = _generate_token(64)
