import json
from database.models import Character, Planet, Vessel, Film

def load_character_data(input_file, session):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)

        planets = ['LV-426', 'Fiorina 161', 'LV-223', 'Earth']

        vessels = ['USM Auriga', 'the Betty', 'USCSS Prometheus', 'USS Sulaco', 'USCSS Nostromo', 'USCSS Patna']

        films = ['Alien Resurrection', 'Prometheus', 'Alien 3', 'Alien', 'Aliens']

        planet_objects = {}
        vessel_objects ={}
        film_objects = {}

        for planet_name in planets:
            planet = Planet(name=planet_name)
            session.add(planet)
            planet_objects[planet_name] = planet

        for vessel_name in vessels:
            vessel = Vessel(name=vessel_name)
            session.add(vessel)
            vessel_objects[vessel_name] = vessel

        for film_name in films:
            film = Film(name=film_name)
            session.add(film) 
            film_objects[film_name] = film

        session.commit()

        for char in data:
            character = Character(
                name=char['name'],
                rank=char['rank'],
                affiliation=char['affiliation'],
                species=char['species'],
                height=char['height'],
                hair=char['hair'],
                eyecolor=char['eyecolor'],
            )

            for planet_name in char.get('planets',[]):
                if planet_name in planet_objects:
                    character.planets.append(planet_objects[planet_name])

            for vessel_name in char.get('vessels',[]):
                if vessel_name in vessel_objects:
                    character.vessels.append(vessel_objects[vessel_name])

            for film_name in char.get('films',[]):
                if film_name in film_objects:
                    character.films.append(film_objects[film_name])

            session.add(character)

        session.commit()
        print(f"Successfully loaded {len(data)} characters to the db")

    except Exception as e:
        session.rollback()
        raise e
