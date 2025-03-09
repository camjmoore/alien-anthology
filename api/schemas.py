from pydantic import BaseModel
from typing import List

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
    rank: str
    affiliation: str
    species: str
    height: str
    hair: str
    eyecolor: str
    planets: List[Planet]
    vessels: List[Vessel]
    films: List[Film]

    class config:
        orm_mode = True
