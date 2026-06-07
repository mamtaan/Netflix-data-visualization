import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# Load Data
df = pd.read_csv("netflix_titles.csv")

# Clean date column
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# Sidebar Filters
st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df['country'].dropna().unique().tolist())
)

year = st.sidebar.slider(
    "Release Year",
    int(df['release_year'].min()),
    int(df['release_year'].max()),
    int(df['release_year'].max())
)

# Apply Filters
filtered_df = df[df['release_year'] <= year]

if country != "All":
    filtered_df = filtered_df[
        filtered_df['country'].str.contains(country, na=False)
    ]

# Title
st.title("🎬 Netflix Dashboard")
st.markdown("Interactive Netflix Data Analysis Dashboard")

# KPI Cards
col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", len(filtered_df[filtered_df['type'] == 'Movie']))
col3.metric("TV Shows", len(filtered_df[filtered_df['type'] == 'TV Show']))

st.markdown("---")

# Movies vs TV Shows
st.subheader("Movies vs TV Shows")

type_counts = filtered_df['type'].value_counts().reset_index()
type_counts.columns = ['Type', 'Count']

fig1 = px.pie(
    type_counts,
    names='Type',
    values='Count',
    hole=0.4
)

st.plotly_chart(fig1, use_container_width=True)

# Top 10 Countries
st.subheader("Top 10 Countries")

country_counts = (
    filtered_df['country']
    .dropna()
    .str.split(',')
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
)

fig2 = px.bar(
    x=country_counts.values,
    y=country_counts.index,
    orientation='h',
    labels={'x': 'Titles', 'y': 'Country'}
)

st.plotly_chart(fig2, use_container_width=True)

# Top 10 Genres
st.subheader("Top 10 Genres")

genre_counts = (
    filtered_df['listed_in']
    .str.split(',')
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
)

fig3 = px.bar(
    x=genre_counts.values,
    y=genre_counts.index,
    orientation='h',
    labels={'x': 'Titles', 'y': 'Genre'}
)

st.plotly_chart(fig3, use_container_width=True)

# Content Added by Year
st.subheader("Content Added Over Time")

year_added = (
    filtered_df['date_added']
    .dt.year
    .value_counts()
    .sort_index()
)

fig4 = px.line(
    x=year_added.index,
    y=year_added.values,
    labels={'x': 'Year', 'y': 'Titles Added'}
)

st.plotly_chart(fig4, use_container_width=True)
