import pickle
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Try to load old pickles and resave with current pandas version
files_to_fix = ['popular.pkl', 'pt.pkl', 'books.pkl', 'similarity_scores.pkl']

for file_name in files_to_fix:
    try:
        print(f"Regenerating {file_name}...")
        # Try loading with different protocols
        try:
            with open(file_name, 'rb') as f:
                data = pickle.load(f, encoding='latin1')
        except:
            with open(file_name, 'rb') as f:
                data = pickle.load(f)
        
        # Resave with current protocol
        with open(file_name, 'wb') as f:
            pickle.dump(data, f)
        
        print(f"✓ {file_name} regenerated successfully")
    except Exception as e:
        print(f"✗ Error with {file_name}: {str(e)}")

print("\nAll pickles regenerated!")
