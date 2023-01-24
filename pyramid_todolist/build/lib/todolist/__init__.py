''' Entry point of the web application. '''
import os

from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy import register

from todolist.models import Base
import todolist.routes

def get_session_factory(engine):
    ''' Return a generator of database session objects. '''
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory


def get_tm_session(session_factory, transaction_manager):
    ''' Build a session and register it as a transaction-managed session. '''
    dbsession = session_factory()
    register(dbsession, transaction_manager=transaction_manager)
    return dbsession


def main(global_config, **settings):
    ''' Returns a pyramid wsgi application. '''
    config = Configurator(settings=settings)
    config.include('todolist.routes')
    config.include('pyramid_tm')
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    session_factory = get_session_factory(engine)
    Base.metadata.create_all(bind=engine)
    config.registry['dbsession_factory'] = session_factory
    config.add_request_method(
        lambda request: get_tm_session(session_factory, request.tm),
        'dbsession',
        reify=True
    )
    config.scan()
    return config.make_wsgi_app()
