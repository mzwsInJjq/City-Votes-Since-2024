import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Load the data
gdf = gpd.read_file(r"C:\Users\Chen\Downloads\WA24\WA24.shp")

# Filter the GeoDataFrame to include only Seattle
gdf = gdf[gdf['PrecinctNa'].str.startswith('SEA ')]

# Define the bbox for Seattle
bbox = (-122.4596960, 47.4810022, -122.2244330, 47.7341503)

# Filter the GeoDataFrame to include only precincts within the bbox
gdf = gdf.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]

# Calculate the Democratic margin in each precinct
gdf['PresDemMargin'] = (gdf['PresDem'] - gdf['PresRep']) / gdf['PresTot']

# Create a color map
norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
cmap = plt.get_cmap('bwr_r')  # '_r' reverses the color map

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
gdf.plot(column='PresDemMargin', cmap=cmap, linewidth=0, ax=ax, norm=norm)

# Set the axis limits to match the bounding box
ax.set_xlim(bbox[0], bbox[2])
ax.set_ylim(bbox[1], bbox[3])

# Remove axis
ax.axis('off')

plt.savefig('seattle_city_election_2024.pdf', format='pdf', bbox_inches='tight')

