import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --------- Load and prep data ---------
@st.cache_data
def load_data():
    df = pd.read_csv("streetview_history.csv")
    return df

df = load_data()

# --------- Streamlit layout ---------
st.set_page_config(layout="wide")
st.title("📸 Project")

st.markdown("""
This dashboard visualizes **Street View coverage of walkable paths in NYC parks**.  
Each point on the map represents a sampled location within a park. Points are checked for Street View coverage using the Google Street View metadata API.  
You can search for a park below and explore its coverage on the map. Green means Street View is available; red means it's not.
""")

# --------- Park selection ---------
park_list = sorted(df["park"].dropna().unique())
selected_park = st.selectbox("Search for a park", park_list)

df_park = df[df["park"] == selected_park]

# --------- Layout: side-by-side ---------
col1, col2 = st.columns(2)

# --------- FOLIUM MAP (Left) ---------
with col1:
    st.subheader("🗺️ Street View Coverage Map")

    # Center map on the park
    center_lat = df_park["lat"].mean()
    center_lon = df_park["lon"].mean()
    fmap = folium.Map(location=[center_lat, center_lon], zoom_start=17)

    # Add points (no clustering)
    for _, row in df_park.iterrows():
        color = "green" if row["streetview_available"] else "red"
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=4,
            color=color,
            fill=True,
            fill_opacity=0.8,
            popup=f"{'✅' if row['streetview_available'] else '❌'} Street View"
        ).add_to(fmap)

    st_data = st_folium(fmap, width=700, height=500)

# --------- GOOGLE MAPS IFRAME (Right) ---------
with col2:
    st.subheader("🌐 Google Maps View (with Street View Layer)")

    # Embed Google Maps with SV layer
    iframe_html = f"""
    <iframe
        src="https://www.google.com/maps?q={center_lat},{center_lon}&layer=c&z=18&output=embed"
        width="700"
        height="500"
        style="border:0;"
        allowfullscreen=""
        loading="lazy"
    ></iframe>
    """
    st.markdown(iframe_html, unsafe_allow_html=True)

    st.markdown(
        f'[🧭 Open full map in Google Maps](https://www.google.com/maps/@?api=1&map_action=map&center={center_lat},{center_lon}&zoom=18&layer=c)',
        unsafe_allow_html=True
    )
