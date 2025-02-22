import json

# TODO!
# "The Alien" and "MU/TH/UR" are still in output

def extract_characters(file, output_file):
    with open(file, 'r') as f:
        data = json.load(f)

    # Extract characters with Species property of "Human"
    character_data = []

    for char in data:
        if char['name'] != "The Alien" and char['name'] != "MU/TH/UR 6000":
            if char['species'] == "Human" or char['species'] == "Synthetic" or char['species'] is None:
                character_data.append(char)

    with open(output_file, 'w') as f_out:
        json.dump(character_data, f_out, indent=4)

if __name__ == "__main__":
    extract_characters("../data/processed/characters_merged.json", "../data/processed/characters_extracted.json")

