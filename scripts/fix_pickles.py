import pickle
import sys
import io

# Custom unpickler to handle pandas BlockPlacement issue
class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if module == 'pandas._libs.internals' and name == 'BlockPlacement':
            # Return a dummy class that accepts slice objects
            class BlockPlacementFix:
                def __init__(self, *args, **kwargs):
                    self.value = args[0] if args else kwargs.get('value')
            return BlockPlacementFix
        return super().find_class(module, name)

def load_pickle_with_workaround(filename):
    """Load pickle file with workaround for pandas compatibility issues"""
    try:
        with open(filename, 'rb') as f:
            # Try normal load first
            try:
                data = pickle.load(f)
                return data
            except TypeError as e:
                if "BlockPlacement" in str(e):
                    # Use custom unpickler for BlockPlacement issues
                    f.seek(0)
                    unpickler = CustomUnpickler(f, encoding='latin1')
                    data = unpickler.load()
                    return data
                raise
    except Exception as e:
        print(f"Error loading {filename}: {str(e)}")
        return None

# Try to fix the pickles
print("Attempting to fix pickle files...")
files = ['popular.pkl', 'pt.pkl', 'books.pkl']

for filename in files:
    try:
        print(f"\nProcessing {filename}...")
        data = load_pickle_with_workaround(filename)
        if data is not None:
            # Resave with current pandas
            with open(filename, 'wb') as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
            print(f"✓ {filename} fixed successfully")
    except Exception as e:
        print(f"✗ Could not fix {filename}: {str(e)}")

print("\nDone!")
