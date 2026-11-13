import geopandas as gpd
import pandas as pd
import requests

# 1. Ingest Data: Download public GeoJSON from the internet
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
print("Ingesting spatial data...")
response = requests.get(url)
data = response.json()

# Convert raw response into a GeoDataFrame
gdf = gpd.GeoDataFrame.from_features(data["features"])

# 2. Data Treatment / Processing
print("Processing and cleaning spatial data...")
# Drop rows without valid geometry
gdf = gdf.dropna(subset=["geometry"])

# Extract coordinates for manipulation
gdf["longitude"] = gdf.geometry.x
gdf["latitude"] = gdf.geometry.y

# Filter out missing magnitude values if present
if "mag" in gdf.columns:
    gdf = gdf[gdf["mag"].notna()]
    processed_gdf = gdf[["mag", "place", "time", "longitude", "latitude", "geometry"]]
else:
    processed_gdf = gdf

# Export cleaned data
processed_gdf.to_file("processed_earthquakes.geojson", driver="GeoJSON")
print(f"Data treatment complete. Saved {len(processed_gdf)} valid spatial records.")