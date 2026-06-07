import streamlit as st
import pandas as pd

st.set_page_config(page_title="Netflix Dashboard", layout="wide")

st.title("🎬 Netflix Dashboard")

# Load data
df = pd.read_csv("netflix_titles.csv")

# Filters
country = st.sidebar.selectbox(
    "Country",
    ["All"] + sorted(df["country"].dropna().unique().tolist())
)

year = st.sidebar.slider(
    "Release Year",
    int(df["release_year"].min()),
    int(df["release_year"].max()),
    int(df["release_year"].max())
)

# Apply filters
filtered_df = df[df["release_year"] <= year]

if country != "All":
    filtered_df = filtered_df[
        filtered_df["country"].str.contains(country, na=False)
    ]

st.subheader("Filtered Dataset")
st.dataframe(filtered_df)

st.subheader("Content Type Distribution")
st.bar_chart(filtered_df["type"].value_counts())
