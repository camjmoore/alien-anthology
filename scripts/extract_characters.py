import json

def extract_characters(file, output_file):
    with open(file, 'r') as f:
        data = json.load(f)

    # Extract characters with Species property of "Human"
    character_data = [char for char in data if char['species'] == "Human" or char['species'] == "Synthetic" or char['species'] is None]

    with open(output_file, 'w') as f_out:
        json.dump(character_data, f_out, indent=4)

if __name__ == "__main__":
    extract_characters("../data/processed/characters_merged.json", "../data/processed/characters_extracted.json")

