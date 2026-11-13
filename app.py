import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Spatial Data Dashboard", layout="wide")

st.title("Interactive Spatial Data Dashboard")
st.markdown("This dashboard ingests, cleans, and visualizes spatial data using `uv`, Streamlit, and Folium.")

# Load processed data
@st.cache_data
def load_data():
    return gpd.read_file("processed_earthquakes.geojson")

try:
    df = load_data()
except Exception as e:
    st.error("Processed data not found. Please run the data ingestion script first.")
    st.stop()

# Sidebar Controls for Data Filtering
st.sidebar.header("Dashboard Filters")
if "mag" in df.columns:
    min_mag = float(df["mag"].min())
    max_mag = float(df["mag"].max())
    selected_mag = st.sidebar.slider("Minimum Magnitude", min_mag, max_mag, min_mag)
    filtered_df = df[df["mag"] >= selected_mag]
else:
    filtered_df = df

st.sidebar.metric(label="Records Displayed", value=len(filtered_df))

# Initialize Folium Interactive Map
#m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")
m = folium.Map(
    location=[20, 0],
    zoom_start=2,
    tiles="OpenStreetMap",
    control_scale=True
)
# Plot coordinates onto the interactive map
for idx, row in filtered_df.iterrows():
    popup_text = f"<b>Location:</b> {row.get('place', 'N/A')}<br><b>Magnitude:</b> {row.get('mag', 'N/A')}"
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=5,
        color="crimson",
        fill=True,
        fill_color="crimson",
        popup=popup_text
    ).add_to(m)

# Render map inside Streamlit
st_data = st_folium(m, width=1100, height=550)