# King County with Natural Shoreline for Puget Sound and Lake Washington
# https://gis-kingcounty.opendata.arcgis.com/datasets/0d91258e15c1457cb4126fbc27507a08_123

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Load the data
gdf = gpd.read_file(r"C:\Users\Chen\Downloads\WA-precincts-with-results.geojson")
king_county = gpd.read_file(r"C:\Users\Chen\Downloads\King_County_with_Natural_Shoreline_for_Puget_Sound_and_Lake_Washington___kingsh_area.geojson")

# Filter precincts by gdf['GEOID']
gdf = gdf[gdf['GEOID'].str.startswith('53033-SEA ')]
gdf = gpd.overlay(gdf, king_county, how='intersection', keep_geom_type=False)

# Define the bbox for Seattle
bbox = (-122.4596960, 47.4810022, -122.2244330, 47.7341503)

# Filter the GeoDataFrame to include only precincts within the bbox
gdf = gdf.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]

# Create a color map
norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
cmap = plt.get_cmap('bwr_r')  # '_r' reverses the color map

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
gdf.plot(column='pct_dem_lead', cmap=cmap, linewidth=0, ax=ax, norm=norm)

# Set the axis limits to match the bounding box
ax.set_xlim(bbox[0], bbox[2])
ax.set_ylim(bbox[1], bbox[3])

# Remove axis
ax.axis('off')

plt.savefig('seattle_city_election_2024.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()