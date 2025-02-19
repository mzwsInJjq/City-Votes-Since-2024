import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Load the data
gdf = gpd.read_file(r"C:\Users\Chen\Downloads\GA-precincts-with-results.geojson")

# Filter precincts by gdf['GEOID']
gdf = gdf[gdf['GEOID'].str.startswith('13121') | gdf['GEOID'].str.startswith('13089')]

dekalb_atl = ['BB', 'BR', 'CX', 'CN', 'EA', 'JA', 'LE', 'MT', 'ER', 'DH']
dekalb_atl_precincts = [f"13089-{pct}" for pct in dekalb_atl]
gdf = gdf[gdf['GEOID'].str.match(r'13121-\d{2}') | gdf['GEOID'].isin(dekalb_atl_precincts)]

# Define the bbox for Atlanta
bbox = (-84.5508540, 33.6478080, -84.2895600, 33.8868230)

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

plt.savefig('atlanta_city_election_2024.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()

sum_votes_dem = gdf['votes_dem'].sum()
sum_votes_rep = gdf['votes_rep'].sum()
sum_votes_third_party = gdf['votes_total'].sum() - sum_votes_dem - sum_votes_rep
sum_votes_total = gdf['votes_total'].sum()
print(f"Democratic % for Atlanta: {100 * sum_votes_dem/sum_votes_total:.2f}%")
print(f"Republican % for Atlanta: {100 * sum_votes_rep/sum_votes_total:.2f}%")
print(f"Third Party % for Atlanta: {100 * sum_votes_third_party/sum_votes_total:.2f}%")