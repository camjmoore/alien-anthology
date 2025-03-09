from api.schemas import CharacterRead
from shared.database.models import Character
from shared.database.connection import create_session
from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/characters", response_model=List[CharacterRead])
def read_characters(skip: int=0, limit: int=100, session: Session=Depends(create_session)):
    characters = session.query(Character).offset(skip).limit(limit).all()
    return characters
