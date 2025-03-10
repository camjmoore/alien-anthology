from pydantic import BaseModel
from typing import List, Optional

class RelationshipRead(BaseModel):
    id: int
    name: str

    class config:
        orm_mode = True

class Planet(RelationshipRead):
    pass

class Vessel(RelationshipRead):
    pass

class Film(RelationshipRead):
    pass

class CharacterRead(BaseModel):
    id: int
    name: str
    rank: Optional[str] = None
    affiliation: Optional[str] = None
    species: Optional[str] = None
    height: Optional[str] = None
    hair: Optional[str] = None
    eyecolor: Optional[str] = None
    planets: List[Planet] = []
    vessels: List[Vessel] = []
    films: List[Film] = []

    class config:
        orm_mode = True
