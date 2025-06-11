from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine(connection_string: str):
    return create_engine(connection_string)


def get_session_factory(connection_string: str):
    engine = get_engine(connection_string)
    return sessionmaker(bind=engine)
