from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

def initialize_db(db_path):
    # Initialize the database
    engine = create_engine(f'sqlite:///{db_path}')
    # Create tables
    Base.metadata.create_all(engine)
    return engine

def create_session(engine):
    # Create a session instance
    Session = sessionmaker(engine)
    return Session()
