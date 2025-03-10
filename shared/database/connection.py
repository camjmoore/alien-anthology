from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import yaml

def initialize_db(db_path):
    # Initialize the database
    engine = create_engine(f'sqlite:///{db_path}')
    # Create tables
    Base.metadata.create_all(engine)
    return engine

def create_session(engine):
    # Create a session instance (for pipeline)
    Session = sessionmaker(engine)
    return Session()

def get_session():
    # Create a callable session instance (for FastAPI)
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
        engine = initialize_db(config['sqlite']['database_path'])
        session = create_session(engine)
    return session
