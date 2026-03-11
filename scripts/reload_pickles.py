"""Regenerate pickle files using pd.read_pickle with compatibility handling"""
import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings('ignore')

def try_load_pickle(filename):
    """Try multiple methods to load a pickle file"""
    methods = [
        lambda: pickle.load(open(filename, 'rb')),
        lambda: pd.read_pickle(filename),
        lambda: pd.read_pickle(filename, compression=None),
        lambda: pickle.load(open(filename, 'rb'), encoding='latin1'),
    ]
    
    for i, method in enumerate(methods):
        try:
            print(f"  Method {i+1}: ", end='')
            result = method()
            print("✓ Success!")
            return result
        except Exception as e:
            print(f"Failed ({type(e).__name__})")
    
    return None

print("Attempting to reload and resave pickle files...\n")

files = {
    'popular.pkl': 'DataFrame',
    'pt.pkl': 'DataFrame (pivot table)',
    'books.pkl': 'DataFrame',
    'similarity_scores.pkl': 'NumPy array'
}

for filename, description in files.items():
    print(f"Processing {filename} ({description})...")
    try:
        data = try_load_pickle(filename)
        
        if data is not None:
            # Resave with current protocol
            with open(filename, 'wb') as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
            print(f"✓ Resaved {filename}\n")
        else:
            print(f"✗ Could not load {filename}\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")

print("Done!")
