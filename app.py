import streamlit as st
import pandas as pd

# ---- Page Config ----
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# ---- Custom CSS ----
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #FFFFFF;
    }

    .stApp {
        background-color: #121212;
        color: #FFFFFF;
    }

    /* HEADINGS */
    h1, h2, h3, h4, h5, h6 {
        color: #00BFFF;
    }

    /* SIDEBAR */
    .css-1d391kg, .css-1cpxqw2 {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border-right: 1px solid #333333;
    }

    /* BUTTONS */
    .stButton>button {
        background-color: #00BFFF;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: bold;
        transition: background-color 0.3s;
    }

    .stButton>button:hover {
        background-color: #00CED1;
        color: white;
    }

    /* TEXT & LABELS */
    .css-10trblm, .css-1v3fvcr, .css-1cpxqw2 {
        color: #FFFFFF !important;
    }

    /* INPUTS */
    input, textarea, .stTextInput>div>div>input, .stSelectbox>div>div>div>input {
        background-color: #1E1E1E;
        color: #FFFFFF;
        border: 1px solid #333333;
        border-radius: 5px;
    }

    /* SLIDERS */
    .stSlider>div>div>div {
        background-color: #00BFFF;
    }

    /* ALERTS */
    .stAlert {
        background-color: #1E1E1E;
        border-left: 5px solid #00BFFF;
        color: white;
    }

    /* DATAFRAME */
    .stDataFrame {
        background-color: #1E1E1E;
        color: #FFFFFF;
        border: 1px solid #333333;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Sidebar Navigation ----
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Explore", "Recommend"])

# ---- Home Page ----
if page == "Home":
    st.markdown("# 🎬 Movie Recommendation System")
    # st.markdown("### _Built with 💖 using Streamlit_")
    st.image("https://cdn-icons-png.flaticon.com/512/744/744922.png", width=100)
    st.write("---")
    st.markdown("Welcome to a smart recommendation system that helps you discover movies you’ll love.")

# ---- Explore Data Page ----
elif page == "Explore":
    st.markdown("## 🔍 Explore Dataset")

    # Load data
    try:
        movies = pd.read_csv('ml-100k/u.item', sep='|', encoding='latin-1', header=None)
        ratings = pd.read_csv('ml-100k/u.data', sep='\t', header=None)
        
        movies.columns = ['movie_id', 'movie_title', 'release_date', 'video_release_date', 'IMDb_URL'] + [f'genre{i}' for i in range(19)]
        ratings.columns = ['user_id', 'movie_id', 'rating', 'timestamp']
        
        movie_ratings = pd.merge(ratings, movies, on='movie_id')

        st.write("### Sample Data")
        st.dataframe(movie_ratings.head())

        st.write("### Rating Statistics")
        st.write(movie_ratings['rating'].describe())

        st.write("### Top 10 Most Rated Movies")
        top_movies = movie_ratings['movie_title'].value_counts().head(10)
        st.write(top_movies)

    except Exception as e:
        st.error("Error loading data. Make sure 'ml-100k' folder is present.")
        st.exception(e)

# ---- Recommendation Page ----
elif page == "Recommend":
    st.markdown("## 🎯 Get Movie Recommendations")
    
    genre = st.selectbox("Choose Genre", ["All", "Action", "Comedy", "Drama", "Romance", "Horror"])
    min_rating = st.slider("Minimum Rating", 1, 5, 3)
    num_results = st.slider("Number of Movies", 5, 20, 10)

    try:
        all_movies = pd.read_csv('ml-100k/u.item', sep='|', encoding='latin-1', header=None)
        all_movies.columns = ['movie_id', 'movie_title', 'release_date', 'video_release_date', 'IMDb_URL'] + [f'genre{i}' for i in range(19)]
        movie_titles = all_movies['movie_title'].tolist()
    except:
        movie_titles = []

    st.markdown("### 🎥 Select Movies You've Already Watched")
    watched_movies = st.multiselect("Choose from the list below:", options=sorted(movie_titles))

    if st.button("🎬 Recommend"):
        st.success(f"Showing top {num_results} {genre} movies with rating >= {min_rating}")

        try:
            movies = pd.read_csv('ml-100k/u.item', sep='|', encoding='latin-1', header=None)
            ratings = pd.read_csv('ml-100k/u.data', sep='\t', header=None)

            movies.columns = ['movie_id', 'movie_title', 'release_date', 'video_release_date', 'IMDb_URL'] + [f'genre{i}' for i in range(19)]
            ratings.columns = ['user_id', 'movie_id', 'rating', 'timestamp']
            
            movie_ratings = pd.merge(ratings, movies, on='movie_id')
            avg_ratings = movie_ratings.groupby('movie_title')['rating'].mean()
            rating_counts = movie_ratings['movie_title'].value_counts()
            filtered = avg_ratings[rating_counts >= 50]
            filtered = filtered[filtered >= min_rating]

            if watched_movies:
                filtered = filtered[~filtered.index.isin(watched_movies)]

            top_recommendations = filtered.sort_values(ascending=False).head(num_results)

            st.write("### Recommended Movies")
            st.dataframe(top_recommendations)

        except:
            st.warning("Dataset not found or error in filtering. Please check your files.")
