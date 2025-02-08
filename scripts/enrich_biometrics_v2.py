import json
import pandas as pd
import numpy as np

def enrich_character_data(input_file, output_file):
    # Read JSON into pandas DataFrame
    df = pd.read_json(input_file)

    # Create random number generator with seed for reproducibility
    rng = np.random.default_rng(seed=42)

    # Get existing non-null values for each attribute
    hair_colors = df['hair'].dropna().unique().tolist()
    heights = df['height'].dropna().unique().tolist()
    eyecolors = df['eyecolor'].dropna().unique().tolist()

    # Replace null values with random selections from existing values
    df['hair'] = df['hair'].apply(
        lambda x: rng.choice(hair_colors) if pd.isna(x) else x
    )

    df['height'] = df['height'].apply(
        lambda x: rng.choice(heights) if pd.isna(x) else x
    )

    df['eyecolor'] = df['eyecolor'].apply(
        lambda x: rng.choice(eyecolors) if pd.isna(x) else x
    )

    # Set species to "Human" if all biometric data is present
    df.loc[df[['hair', 'height', 'eyecolor']].notna().all(axis=1), 'species'] = 'Human'

    # Convert back to JSON and save
    with open(output_file, 'w') as f:
        json.dump(df.to_dict(orient='records'), f, indent=4)

if __name__ == "__main__":
    enrich_character_data("../data/processed/characters_merged.json", 
                          "../data/processed/characters_enriched_bio.json")
