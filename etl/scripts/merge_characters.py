import pandas as pd

#TODO! consider using pandas data frames as primary data structure for scripts

def merge_json(file1, file2, output_file):
    df1 = pd.read_json(file1)
    df2 = pd.read_json(file2)

    df = pd.concat([df1, df2])

    df = df.dropna(subset=['name'])
    df = df.drop_duplicates(subset=['name'])

    df = df[df.name != "David (synthetic model)"]

    df.to_json(output_file, orient='records', indent=4)

if __name__ == "__main__":
    merge_json("../data/raw/anthology_characters.json", 
               "../data/raw/avp_characters.json", 
               "../data/processed/characters_merged.json")
