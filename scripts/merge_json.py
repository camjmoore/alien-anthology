import json

def merge_json(file1, file2, output_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    # Combine both datasets
    merged_data = {character['name']: character for character in (data1 + data2) if character['name'] is not None}

    # Convert back to a list of unique characters
    merged_data_list = list(merged_data.values())

    with open(output_file, 'w') as f_out:
        json.dump(merged_data_list, f_out, indent=4)

if __name__ == "__main__":
    merge_json("../data/raw/anthology_characters.json", "../data/raw/avp_characters.json", "../data/processed/characters_merged.json")

