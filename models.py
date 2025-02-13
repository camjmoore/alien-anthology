from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Junction Tables
character_planets = Table(
    'character_planets', Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id')),
    Column('planet_id', Integer, ForeignKey('planets.id'))
)

character_vessels = Table(
    'character_vessels', Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id')),
    Column('vessel_id', Integer, ForeignKey('vessels.id'))
)

character_films = Table(
    'character_films', Base.metadata,
    Column('character_id', Integer, ForeignKey('characters.id')),
    Column('film_id', Integer, ForeignKey('films.id'))
)

class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    rank = Column(String)
    affiliation = Column(String)
    species = Column(String)
    height = Column(String)
    hair = Column(String)
    eyecolor = Column(String)

    # Relationships
    planets = relationship("Planet", secondary=character_planets, back_populates="characters")
    vessels = relationship("Vessel", secondary=character_vessels, back_populates="characters")
    films = relationship("Film", secondary=character_films, back_populates="characters")

class Planet(Base):
    __tablename__ = 'planets'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship
    characters = relationship("Character", secondary=character_planets, back_populates="planets")

class Vessel(Base):
    __tablename__ = 'vessels'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship
    characters = relationship("Character", secondary=character_vessels, back_populates="vessels")

class Film(Base):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    # Relationship
    characters = relationship("Character", secondary=character_films, back_populates="characters")

