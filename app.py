import streamlit as st
import pandas as pd
import requests

API_KEY = st.secrets["api_key"]  # Get one from http://www.omdbapi.com/apikey.aspx

def get_director(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    try:
        response = requests.get(url).json()
        if response.get("Response") == "True":
            return response.get("Title"), response.get("Director", "N/A"), response.get("Awards", "N/A"), response.get("Year", "N/A"), response.get("Country", "N/A"), response.get("imdbRating", "N/A")
        else:
            return None, "Not found", "N/A", "N/A", "N/A", "N/A"
    except Exception:
        # Return a tuple to match expected unpacking
        return "API Error", "N/A", "N/A", "N/A", "N/A", "N/A"
    
st.set_page_config(
    page_title="Movie Director Finder 🎬",  # Browser tab title
    page_icon="🎥",                         # Favicon (emoji or path to .png/.ico)
    layout="wide"                           # "centered" or "wide"
)

st.title("🎬 Movie Director Finder (Exact Match)")
st.write("Upload a CSV with a column **Title** to fetch directors (exact title match only).")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if "Title" not in df.columns:
        st.error("CSV must contain a column named 'Title'")
    else:
        results = []
        with st.spinner("Fetching directors..."):
            for title in df["Title"]:
                matched, director, awards, year, country, imdbRating = get_director(title)
                results.append({
                    "Input Title": title,
                    "Matched Title": matched if matched else "No match",
                    "Director": director,
                    "Awards": awards,
                    "Year": year,
                    "Country": country,
                    "IMDB Rating": imdbRating
                })

        result_df = pd.DataFrame(results)

        # Show results in app
        st.subheader("📊 Results")
        st.dataframe(result_df)

        # Download button
        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Results CSV",
            data=csv,
            file_name="movies_with_directors.csv",
            mime="text/csv"
        )