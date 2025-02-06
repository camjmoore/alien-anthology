import json

def enrich_character_data(input_file, output_file):

    with open(input_file, 'r') as f:
        characters = json.load(f)

    hair_colors = []
    heights = []
    eyecolors = []
    
    # create a collection of hair colors fom character data
    for char in characters:
        hair = char.get("hair")
        height = char.get("height")
        eyecolor = char.get("eyecolor")

        if hair and hair not in hair_colors:
            hair_colors.append(hair)
        
        if height and height not in heights:
            heights.append(height)

        if eyecolor and eyecolor not in eyecolors:
            eyecolors.append(eyecolor)

        if hair and height and eyecolor:
            char["species"] = "Human"

    with open(output_file, 'w') as f:
        json.dump({'hair_colors': hair_colors, 'heights': heights, 'eyecolors': eyecolors}, f, indent=4)

if __name__ == "__main__":
    enrich_character_data("../data/processed/characters_merged.json", "../data/processed/characters_enriched_biometrics.json")
