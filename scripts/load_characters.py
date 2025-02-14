import json
from database.models import Character, Planet, Vessel, Film

def load_character_data(input_file, session):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
        for _, char in data:
            session.add(char)
            # add data into tables here
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
