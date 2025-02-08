import json
import pandas as pd
import numpy as np

def append_unique(series, value):
    """
    Appends a value to array elements in a pandas Series if it doesn't exist.
    Removes conflicting substrings before appending.
    """
    def process_array(arr):
        if not isinstance(arr, list):
            arr = []
        new_substring = value.split(' ', 1)[-1] if ' ' in value else value
        arr = [item for item in arr if not (
            (' ' in item and item.split(' ', 1)[-1] == new_substring) or 
            item == new_substring
        )]
        if value not in arr:
            arr.append(value)
        return arr
    return series.apply(process_array)

def enrich_character_data(input_file, output_file):
    # Read JSON into DataFrame
    df = pd.read_json(input_file)

    # Create random number generator with seed
    rng = np.random.default_rng(seed=42)

    # Enrich biometric data
    hair_colors = df['hair'].dropna().unique().tolist()
    heights = df['height'].dropna().unique().tolist()
    eyecolors = df['eyecolor'].dropna().unique().tolist()

    df['hair'] = df['hair'].apply(lambda x: rng.choice(hair_colors) if pd.isna(x) else x)
    df['height'] = df['height'].apply(lambda x: rng.choice(heights) if pd.isna(x) else x)
    df['eyecolor'] = df['eyecolor'].apply(lambda x: rng.choice(eyecolors) if pd.isna(x) else x)
    synthetic_mask = df['species'] == 'Synthetic'
    df['species'] = 'Human'
    df.loc[synthetic_mask, 'species'] = 'Synthetic'
    df.loc[df['name'] == 'Ripley 8', 'species'] = 'Human-Xenomorph Hybrid'

    # Enrich Rank and Affiliation
    df['rank'] = df['rank'].fillna("Unknown")
    df['affiliation'] = df['affiliation'].fillna("Unknown")
    df.loc[df['name'] == 'Johner', 'affiliation'] = 'the Betty Crew'
    df.loc[df['name'] == 'Frank Elgyn', 'affiliation'] = 'the Betty Crew'
    df.loc[df['name'] == 'Christie', 'affiliation'] = 'the Betty Crew'
    df.loc[df['name'] == 'Annalee Call', 'affiliation'] = 'the Betty Crew'
    df.loc[df['name'] == 'Christie', 'rank'] = 'Mercenary'
    df.loc[df['name'] == 'Johner', 'rank'] = 'Mercenary'

    df.loc[df['affiliation'] == 'the Betty Crew', 'vessels'] = append_unique(df.loc[df['affiliation'] == 'the Betty Crew'], "The Betty")

    # Initialize vessels and planets columns
    if 'vessels' not in df.columns:
        df['vessels'] = df.apply(lambda x: [], axis=1)
    if 'planets' not in df.columns:
        df['planets'] = df.apply(lambda x: [], axis=1)

    # Enrich based on films
    mask_resurrection = df['films'].apply(lambda x: "Alien Resurrection" in x)
    df.loc[mask_resurrection, 'vessels'] = append_unique(df.loc[mask_resurrection, 'vessels'], "USM Auriga")

    # Special cases
    df.loc[df['name'] == "Ripley 8", 'planets'] = df.loc[df['name'] == "Ripley 8", 'planets'].apply(lambda x: [])
    df.loc[df['name'] == "Annalee Call", 'planets'] = df.loc[df['name'] == "Annalee Call", 'planets'].apply(lambda x: ["Earth"])

    # Prometheus characters
    mask_prometheus = df['films'].apply(lambda x: "Prometheus" in x)
    df.loc[mask_prometheus, 'vessels'] = append_unique(df.loc[mask_prometheus, 'vessels'], "USCSS Prometheus")
    df.loc[mask_prometheus, 'planets'] = append_unique(df.loc[mask_prometheus, 'planets'], "LV-223")
    df.loc[mask_prometheus, 'planets'] = append_unique(df.loc[mask_prometheus, 'planets'], "Earth")

    # Alien 3 characters
    mask_alien3 = df['films'].apply(lambda x: "Alien 3" in x)
    df.loc[mask_alien3, 'planets'] = append_unique(df.loc[mask_alien3, 'planets'], "Fiorina 161 /(Fury/)")

    # Bishop cases
    df.loc[df['name'] == "Bishop", 'vessels'] = append_unique(df.loc[df['name'] == "Bishop", 'vessels'], "USS Sulaco")
    bishop_mask = df['name'] == "Michael Bishop"
    df.loc[bishop_mask, 'vessels'] = append_unique(df.loc[bishop_mask, 'vessels'], "Sulaco")
    df.loc[bishop_mask, 'vessels'] = append_unique(df.loc[bishop_mask, 'vessels'], "USCSS Patna")

    # Alien characters
    mask_alien = df['films'].apply(lambda x: "Alien" in x)
    df.loc[mask_alien, 'vessels'] = append_unique(df.loc[mask_alien, 'vessels'], "USCSS Nostromo")
    df.loc[mask_alien, 'planets'] = append_unique(df.loc[mask_alien, 'planets'], "LV-426 /(Acheron/)")

    # Aliens characters
    mask_aliens = df['films'].apply(lambda x: "Aliens" in x)
    df.loc[mask_aliens, 'vessels'] = append_unique(df.loc[mask_aliens, 'vessels'], "USS Sulaco")
    df.loc[mask_aliens, 'planets'] = append_unique(df.loc[mask_aliens, 'planets'], "LV-426 /(Acheron/)")

    # Save enriched data
    with open(output_file, 'w') as f:
        json.dump(df.to_dict('records'), f, indent=4)

if __name__ == "__main__":
    enrich_character_data("../data/processed/characters_extracted.json", 
                          "../data/processed/characters_enriched.json")

