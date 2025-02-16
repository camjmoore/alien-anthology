import json
from database.models import Character, Planet, Vessel, Film

def load_character_data(input_file, session):
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
    
        planets = ['LV-426', 'Fiorina 161', 'LV-223', 'Earth']

        vessels = ['USM Auriga', 'the Betty', 'USCSS Prometheus', 'USS Sulaco', 'USCSS Nostromo', 'USCSS Patna']

        films = ['Alien Resurrection', 'Prometheus', 'Alien 3', 'Alien', 'Aliens']

        for planet_name in planets:
            session.add(Planet(name=planet_name))

        for vessel_name in vessels:
            session.add(Vessel(name=vessel_name))

        for film_name in films:
            session.add(Film(name=film_name)) 

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
                character.planets.append(planet_name)

            for vessel_name in char.get('vessels',[]):
                character.vessels.append(vessel_name)

            for film_name in char.get('films',[]):
                character.films.append(film_name)

            session.add(character)

        session.commit()
        print(f"Successfully loaded {len(data)} characters to the db")

    except Exception as e:
        session.rollback()
        raise e
