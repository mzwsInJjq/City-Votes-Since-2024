import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Load the data
gdf1 = gpd.read_file(r'C:\Users\Chen\Downloads\NY-precincts-with-results.geojson')
gdf2 = gpd.read_file(r'C:\Users\Chen\Downloads\NJ-precincts-with-results.geojson')

# Concatenate the GeoDataFrames
gdf = gpd.GeoDataFrame(pd.concat([gdf1, gdf2], ignore_index=True))

# Define the bbox for New York City
bbox = (-74.2588430, 40.4765780, -73.7002330, 40.9176300)

# Filter the GeoDataFrame to include only precincts within the bbox
gdf = gdf.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]

# Create a color map
norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
cmap = plt.get_cmap('bwr_r')  # '_r' reverses the color map

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
gdf.plot(column='pct_dem_lead', cmap=cmap, linewidth=0, ax=ax, norm=norm)

# Remove axis
ax.axis('off')

# Set the axis limits to match the bounding box
ax.set_xlim(bbox[0], bbox[2])
ax.set_ylim(bbox[1], bbox[3])

plt.savefig('nyc_city_election_2024.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()