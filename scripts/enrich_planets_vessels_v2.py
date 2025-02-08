import pandas as pd
import json

def append_unique(series, value):
    """
    Appends a value to array elements in a pandas Series if it doesn't exist.
    Removes conflicting substrings before appending.
    """
    def process_array(arr):
        if not isinstance(arr, list):
            arr = []

        # Extract substring after space in new value
        new_substring = value.split(' ', 1)[-1] if ' ' in value else value

        # Remove conflicting items
        arr = [item for item in arr if not (
            (' ' in item and item.split(' ', 1)[-1] == new_substring) or 
            item == new_substring
        )]

        # Append if not exists
        if value not in arr:
            arr.append(value)
        return arr

    return series.apply(process_array)

def enrich_character_data(input_file, output_file):
    # Read JSON into DataFrame
    df = pd.read_json(input_file)

    # Initialize vessels and planets columns if they don't exist
    if 'vessels' not in df.columns:
        df['vessels'] = df.apply(lambda x: [], axis=1)
    if 'planets' not in df.columns:
        df['planets'] = df.apply(lambda x: [], axis=1)

    # Enrich based on films
    mask_resurrection = df['films'].apply(lambda x: "Alien Resurrection" in x)
    df.loc[mask_resurrection, 'vessels'] = append_unique(
        df.loc[mask_resurrection, 'vessels'], 
        "USM Auriga"
    )

    # Special case for Ripley 8
    df.loc[df['name'] == "Ripley 8", 'planets'] = df.loc[
    df['name'] == "Ripley 8", 'planets'
].apply(lambda x: [])

    # Special case for Annalee Call
    df.loc[df['name'] == "Annalee Call", 'planets'] = df.loc[
    df['name'] == "Annalee Call", 'planets'
].apply(lambda x: ["Earth"])

    # Prometheus characters
    mask_prometheus = df['films'].apply(lambda x: "Prometheus" in x)
    df.loc[mask_prometheus, 'vessels'] = append_unique(
        df.loc[mask_prometheus, 'vessels'], 
        "USCSS Prometheus"
    )
    df.loc[mask_prometheus, 'planets'] = append_unique(
        df.loc[mask_prometheus, 'planets'], 
        "LV-223"
    )
    df.loc[mask_prometheus, 'planets'] = append_unique(
        df.loc[mask_prometheus, 'planets'], 
        "Earth"
    )

    # Alien 3 characters
    mask_alien3 = df['films'].apply(lambda x: "Alien 3" in x)
    df.loc[mask_alien3, 'planets'] = append_unique(
        df.loc[mask_alien3, 'planets'], 
        "Fiorina 161 /(Fury/)"
    )

    # Special cases for Bishop and Michael Bishop
    df.loc[df['name'] == "Bishop", 'vessels'] = append_unique(
        df.loc[df['name'] == "Bishop", 'vessels'], 
        "USS Sulaco"
    )

    bishop_mask = df['name'] == "Michael Bishop"
    df.loc[bishop_mask, 'vessels'] = append_unique(
        df.loc[bishop_mask, 'vessels'], 
        "Sulaco"
    )
    df.loc[bishop_mask, 'vessels'] = append_unique(
        df.loc[bishop_mask, 'vessels'], 
        "USCSS Patna"
    )

    # Alien characters
    mask_alien = df['films'].apply(lambda x: "Alien" in x)
    df.loc[mask_alien, 'vessels'] = append_unique(
        df.loc[mask_alien, 'vessels'], 
        "USCSS Nostromo"
    )
    df.loc[mask_alien, 'planets'] = append_unique(
        df.loc[mask_alien, 'planets'], 
        "LV-426 /(Acheron/)"
    )

    # Aliens characters
    mask_aliens = df['films'].apply(lambda x: "Aliens" in x)
    df.loc[mask_aliens, 'vessels'] = append_unique(
        df.loc[mask_aliens, 'vessels'], 
        "USS Sulaco"
    )
    df.loc[mask_aliens, 'planets'] = append_unique(
        df.loc[mask_aliens, 'planets'], 
        "LV-426 /(Acheron/)"
    )

    # Save to JSON
    with open(output_file, 'w') as f_out:
        json.dump(df.to_dict('records'), f_out, indent=4)

if __name__ == "__main__":
    enrich_character_data("../data/processed/characters_enriched_bio.json", 
                          "../data/processed/characters_enriched_bio_pv.json")

