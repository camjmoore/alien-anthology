import json

def enrich_character_data(input_file, output_file):
    def append_unique(array, value):
        """
        Appends a value to an array if it doesn't already exist. 
        Removes any existing items that contain a conflicting substring.
        """
        # Extract the substring after the first space in the new value (if applicable)
        new_substring = value.split(' ', 1)[-1] if ' ' in value else value

        # Remove conflicting items from the array
        array = [item for item in array if not (
            (' ' in item and item.split(' ', 1)[-1] == new_substring) or item == new_substring
        )]

        # Append the new value if it doesn't already exist
        if value not in array:
            array.append(value)

        return array

    with open(input_file, 'r') as f:
        characters = json.load(f)

    for char in characters:
        # Enrich vessels and planets based on films
        if "Alien Resurrection" in char["films"]:
            char["vessels"] = append_unique(char.get("vessels", []), "USM Auriga")
            if char["name"] == "Ripley 8":
                char["planets"] = []
            if char["name"] == "Annalee Call":
                char["planets"] = ["Earth"]

        if "Prometheus" in char["films"]:
            char["vessels"] = append_unique(char.get("vessels", []), "USCSS Prometheus")
            char["planets"] = append_unique(char.get("planets", []), "LV-223")
            char["planets"] = append_unique(char.get("planets", []), "Earth")

        if "Alien 3" in char["films"]:
            char["planets"] = append_unique(char.get("planets", []), "Fiorina 161 /(Fury/)")
            if char["name"] == "Bishop":
                char["vessels"] = append_unique(char.get("vessels", []), "USS Sulaco")
            if char["name"] == "Michael Bishop":
                char["vessels"] = append_unique(char.get("vessels", []), "Sulaco")
                char["vessels"] = append_unique(char["vessels"], "USCSS Patna")
        if "Alien" in char["films"]:
            char["vessels"] = append_unique(char.get("vessels", []), "USCSS Nostromo")
            char["planets"] = append_unique(char.get("planets", []), "LV-426 /(Acheron/)")

        if "Aliens" in char["films"]:
            char["vessels"] = append_unique(char.get("vessels", []), "USS Sulaco")
            char["planets"] = append_unique(char.get("planets", []), "LV-426 /(Acheron/)")

    with open(output_file, 'w') as f_out:
        json.dump(characters, f_out, indent=4)

if __name__ == "__main__":
    enrich_character_data("../data/processed/characters_merged.json", "../data/processed/characters_enriched_pv.json")

