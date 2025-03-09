from pydantic import BaseModel
from typing import List, Optional

class PlanetSchema(BaseModel):
    name: str

class VesselSchema(BaseModel):
    name: str

class FilmSchema(BaseModel):
    name: str

class CharacterSchema(BaseModel):
    name: str
    rank: Optional[str] = None
    affiliation: Optional[str] = None
    species: Optional[str] = None
    height: Optional[str] = None
    hair: Optional[str] = None
    eyecolor: Optional[str] = None
    planets: List[str] = []
    vessels: List[str] = []
    films: List[str] = []
