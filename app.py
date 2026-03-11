from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Try to load pickles with compatibility handling
def load_pickle_safe(filename):
    """Load pickle with Python 3.13 and newer pandas compatibility"""
    try:
        # First attempt: normal load
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except TypeError as e:
        if "BlockPlacement" in str(e):
            # Try with encoding to work around pandas BlockPlacement issue
            try:
                import io
                with open(filename, 'rb') as f:
                    data = f.read()
                return pickle.loads(data, encoding='latin1')
            except:
                pass
        raise

try:
    popular_df = load_pickle_safe('data/popular.pkl')
    pt = load_pickle_safe('data/pt.pkl')
    books = load_pickle_safe('data/books.pkl')
    similarity_scores = load_pickle_safe('data/similarity_scores.pkl')
except Exception as e:
    print(f"Error loading pickles: {e}")
    print("Using fallback data...")
    # Create empty fallback data structures
    popular_df = pd.DataFrame({
        'Book-Title': ['Sample Book'],
        'Book-Author': ['Sample Author'],
        'Image-URL-M': [''],
        'num_ratings': [0],
        'avg_rating': [0.0]
    })
    pt = pd.DataFrame()
    books = pd.DataFrame({'Book-Title': [], 'Book-Author': [], 'Image-URL-M': []})
    similarity_scores = np.array([])

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)