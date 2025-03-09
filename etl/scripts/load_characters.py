import json
from shared.database.models import Character, Planet, Vessel, Film
from shared.database.schemas import CharacterSchema, PlanetSchema, VesselSchema, FilmSchema

def load_character_data(input_file, session):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
            #Character data schema validation
            characters = [CharacterSchema(**char) for char in data]

        planet_names = ['LV-426', 'Fiorina 161', 'LV-223', 'Earth']

        vessel_names = ['USM Auriga', 'the Betty', 'USCSS Prometheus', 'USS Sulaco', 'USCSS Nostromo', 'USCSS Patna']

        film_names = ['Alien Resurrection', 'Prometheus', 'Alien 3', 'Alien', 'Aliens']

        #Planets, Vessels, Films data schema validation
        planets = [PlanetSchema(name=p_name) for p_name in planet_names]
        vessels = [VesselSchema(name=v_name) for v_name in vessel_names]
        films = [FilmSchema(name=f_name) for f_name in film_names]

        #Saved model instantiations
        planet_objects = {}
        vessel_objects ={}
        film_objects = {}

        #Instantiate models from validated data
        for p in planets:
            planet = Planet(name=p.name)
            session.add(planet)
            planet_objects[p.name] = planet

        for v in vessels:
            vessel = Vessel(name=v.name)
            session.add(vessel)
            vessel_objects[v.name] = vessel

        for f in films:
            film = Film(name=f.name)
            session.add(film) 
            film_objects[f.name] = film

        #single session.commit more efficient than session.flush after every session.add
        session.commit()

        #Instantiate Character models from validated data and populate relationships
        for char in characters:
            character = Character(
                name=char.name,
                rank=char.rank,
                affiliation=char.affiliation,
                species=char.species,
                height=char.height,
                hair=char.hair,
                eyecolor=char.eyecolor,
            )

            #Append saved model instantiations to appropriate character instantiation
            for name in char.planets:
                if name in planet_objects:
                    character.planets.append(planet_objects[name])

            for name in char.vessels:
                if name in vessel_objects:
                    character.vessels.append(vessel_objects[name])

            for name in char.films:
                if name in film_objects:
                    character.films.append(film_objects[name])

            session.add(character)

        session.commit()
        print(f"Successfully loaded {len(data)} characters to the db")

    except Exception as e:
        session.rollback()
        raise e
