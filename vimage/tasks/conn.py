# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from vimage.extensions import fsk_celery


def connect():
    """Connects to the database and return a session"""

    # uri = 'mysql+pymysql://root:@localhost/mixshopy'

    uri = fsk_celery.conf['SQLALCHEMY_DATABASE_URI']

    # The return value of create_engine() is our connection object
    some_engine = create_engine(uri)

    # create a session
    some_session = scoped_session(sessionmaker(bind=some_engine))

    return some_engine, some_session


conn, session = connect()