import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide")

st.markdown("""
<style>

/* ===== BACKGROUND ===== */
.stApp {
    background-color: #141414;
}

/* ===== TEXT FIX (MAIN ISSUE) ===== */
html, body, .stApp, .block-container {
    color: white !important;
}

/* HEADINGS */
h1, h2, h3, h4 {
    color: white !important;
}

/* PARAGRAPH */
p, span, label {
    color: #e5e5e5 !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #1f1f1f;
}

/* ===== DROPDOWN (FINAL WORKING FIX) ===== */

/* Selected box */
div[data-baseweb="select"] > div {
    background-color: white !important;
    color: black !important;
}

/* Selected text */
div[data-baseweb="select"] span {
    color: black !important;
}

/* Dropdown list */
div[role="listbox"] {
    background-color: white !important;
}

/* Options */
div[role="option"] {
    color: black !important;
}

/* Hover */
div[role="option"]:hover {
    background-color: #eeeeee !important;
}

/* Selected option */
div[role="option"][aria-selected="true"] {
    background-color: #E50914 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA
# =========================
data = pd.read_csv("data/processed/dashboard_data.csv")

# =========================
# HEADER
# =========================
st.title("🎬 Netflix Content Analysis Dashboard")
st.markdown("### Explore Netflix content trends with interactive filters")
st.markdown("---")

# =========================
# SEARCH BAR
# =========================

st.subheader("🔍 Search Content")

search = st.text_input("Enter movie or show name")

if search:
    result = data[data['title'].str.contains(search, case=False, na=False)]
    st.write(result[['title', 'release_year', 'main_genre']].head(5))

st.markdown("---")


# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🎯 Filters")

genre = st.sidebar.selectbox(
    "Select Genre",
    ["All"] + sorted(data['main_genre'].dropna().astype(str).unique())
)

country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(data['main_country'].dropna().astype(str).unique())
)

content_type = st.sidebar.selectbox(
    "Select Content Type",
    ["All"] + list(data['type'].dropna().unique())
)

year = st.sidebar.slider(
    "Release Year",
    int(data['release_year'].min()),
    int(data['release_year'].max()),
    2010
)

# =========================
# FILTER LOGIC
# =========================
filtered = data.copy()

if genre != "All":
    filtered = filtered[filtered['main_genre'] == genre]

if country != "All":
    filtered = filtered[filtered['main_country'] == country]

if content_type != "All":
    filtered = filtered[filtered['type'] == content_type]

filtered = filtered[filtered['release_year'] >= year]

st.caption(f"Filtered rows: {len(filtered)}")

if filtered.empty:
    st.warning("No data available for selected filters")
    st.stop()

    filtered = data.copy()

if genre != "All":
    filtered = filtered[filtered['main_genre'] == genre]

if country != "All":
    filtered = filtered[filtered['main_country'] == country]

if content_type != "All":
    filtered = filtered[filtered['type'] == content_type]

filtered = filtered[filtered['release_year'] >= year]


# =========================
# 😊 PICK YOUR MOOD (FINAL CLEAN)
# =========================

st.subheader("😊 Pick Your Mood")

mood = st.selectbox(
    "How are you feeling?",
    ["Select Mood", "Happy 😄", "Sad 😢", "Excited 🤩", "Relaxed 😌", "Thriller 😨"]
)

# STOP if nothing selected
if mood == "Select Mood":
    st.info("👆 Select a mood to get recommendations")
else:
    mood_map = {
        "Happy 😄": "Comedies",
        "Sad 😢": "Dramas",
        "Excited 🤩": "Action & Adventure",
        "Relaxed 😌": "Documentaries",
        "Thriller 😨": "Horror Movies"
    }

    selected_genre = mood_map[mood]

    if selected_genre not in filtered['main_genre'].unique():
        st.warning("No matching data for this mood")
    else:
        mood_data = filtered[filtered['main_genre'] == selected_genre]

        st.markdown(f"### 🎬 Showing {selected_genre} content")

        if len(mood_data) == 0:
            st.warning("No content found for selected filters")
        else:
            mood_data = mood_data.sample(min(5, len(mood_data)))

            for _, row in mood_data.iterrows():
                st.markdown(f"""
                <div style="
                    background-color:#1f1f1f;
                    padding:12px;
                    border-radius:10px;
                    margin-bottom:10px;
                ">
                    <b>🎬 {row['title']}</b><br>
                    📅 {row['release_year']} |
                    🎭 {row['main_genre']} |
                    🌍 {row['main_country']}
                </div>
                """, unsafe_allow_html=True)

st.markdown("---")
    # =========================
# TOP PICKS
# =========================
# =========================
# 🎯 TOP PICKS FOR YOU (SMART VERSION)
# =========================

st.subheader("🎯 Top Picks For You")

top_picks = filtered.sort_values(by='release_year', ascending=False).head(5)

if len(top_picks) == 0:
    st.warning("No content available based on selected filters")
else:
    titles = top_picks['title'].tolist()

    selected_title = st.selectbox("Choose a title to explore", titles)

    selected_data = top_picks[top_picks['title'] == selected_title].iloc[0]

    st.markdown(f"""
    <div style="
        background:#1f1f1f;
        padding:15px;
        border-radius:12px;
        border-left:5px solid #4dabf7;
    ">
        <h4>🎬 {selected_data['title']}</h4>
        <p>📅 {selected_data['release_year']}</p>
        <p>🎭 {selected_data['main_genre']}</p>
        <p>🌍 {selected_data['main_country']}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
# =========================
# TRENDING NOW
# =========================
st.subheader("🔥 Trending Now")

top_genres = filtered['main_genre'].value_counts().head(5)

cols = st.columns(5)

for i, (genre, count) in enumerate(top_genres.items()):
    with cols[i]:
        st.markdown(f"""
        <div style="
            background: #1f1f1f;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid #333;
        ">
            <h4 style="color:white;">{genre}</h4>
            <p style="color:gray;">{count} titles</p>
        </div>
        """, unsafe_allow_html=True)
  

# =========================
# KPIs
# =========================
st.markdown("## 📊 Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Titles", len(filtered))

with col2:
    st.metric("Movies", len(filtered[filtered['type']=="Movie"]))

with col3:
    st.metric("TV Shows", len(filtered[filtered['type']=="TV Show"]))
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")


# =========================
# CHARTS
# =========================

# -------- Row 1 --------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Genres")
    genre_counts = filtered['main_genre'].value_counts().head(10)

    fig, ax = plt.subplots()
    ax.bar(genre_counts.index, genre_counts.values, color='#4dabf7')

    ax.tick_params(axis='x', rotation=45, colors='white')
    ax.tick_params(axis='y', colors='white')

    fig.patch.set_facecolor('#141414')
    ax.set_facecolor('#141414')

    st.pyplot(fig)

with col2:
    st.subheader("Top Countries")
    country_counts = filtered['main_country'].value_counts().head(10)

    fig, ax = plt.subplots()
    ax.barh(country_counts.index, country_counts.values, color='#4dabf7')

    ax.tick_params(colors='white')

    fig.patch.set_facecolor('#141414')
    ax.set_facecolor('#141414')

    st.pyplot(fig)

# -------- Row 2 --------
col3, col4 = st.columns(2)

with col3:
    st.subheader("Rating Distribution")
    rating_counts = filtered['rating'].value_counts()

    fig, ax = plt.subplots()
    ax.bar(rating_counts.index, rating_counts.values, color='#4dabf7')

    ax.tick_params(axis='x', rotation=45, colors='white')
    ax.tick_params(axis='y', colors='white')

    fig.patch.set_facecolor('#141414')
    ax.set_facecolor('#141414')

    st.pyplot(fig)

with col4:
    st.subheader("Content Growth Over Time")
    year_counts = filtered['year_added'].value_counts().sort_index()

    fig, ax = plt.subplots()
    ax.plot(year_counts.index, year_counts.values, marker='o', color='#4dabf7')

    ax.tick_params(colors='white')

    fig.patch.set_facecolor('#141414')
    ax.set_facecolor('#141414')

    st.pyplot(fig)

# =========================
# HISTOGRAM
# =========================
st.subheader("Movie Duration Distribution")

movie_data = filtered[filtered['type'] == "Movie"]

fig, ax = plt.subplots()
ax.hist(movie_data['duration_int'], bins=20, color='#4dabf7')

ax.tick_params(colors='white')

fig.patch.set_facecolor('#141414')
ax.set_facecolor('#141414')

st.pyplot(fig)

# =========================
# TOP GENRE PER YEAR
# =========================
st.subheader("Top Genre per Year")

top_genre_year = (
    filtered.groupby(['year_added', 'main_genre'])
    .size()
    .reset_index(name='count')
)

top_genre_year = top_genre_year.loc[
    top_genre_year.groupby('year_added')['count'].idxmax()
]

fig, ax = plt.subplots()

ax.plot(top_genre_year['year_added'], top_genre_year['count'],
        marker='o', color='#4dabf7')

ax.tick_params(colors='white')

fig.patch.set_facecolor('#141414')
ax.set_facecolor('#141414')

st.pyplot(fig)

st.markdown("---")
