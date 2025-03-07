from shared.database.connection import initialize_db
from shared.database.connection import create_session
from etl.scripts.merge_characters import merge_json
from etl.scripts.extract_characters import extract_characters
from etl.scripts.enrich_characters import enrich_character_data
from etl.scripts.load_characters import load_character_data
import yaml

def run_pipeline():

    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

        engine = initialize_db(config['sqlite']['database_path'])
        session = create_session(engine)

        merge_json(config['data']['raw']['anthology_characters'], config['data']['raw']['avp_characters'], config['data']['processed']['merged'])

        extract_characters(config['data']['processed']['merged'], config['data']['processed']['extracted'])

        enrich_character_data(config['data']['processed']['extracted'], config['data']['processed']['enriched'])

        load_character_data(config['data']['processed']['enriched'], session)

if __name__ == "__main__":
    run_pipeline()
