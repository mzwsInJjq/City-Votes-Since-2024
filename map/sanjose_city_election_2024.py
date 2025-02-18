import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import requests
from io import BytesIO

# URL of the XLS file
url = "https://gis.sanjoseca.gov/apps/redistricting/PDFs/SanJoseDraftPlanFinal_VotingPrecincts_122221.xlsx"

# Download the file
response = requests.get(url)
if response.status_code != 200:
    raise Exception("Failed to download the XLS file")

# Load the Excel file into a DataFrame
df = pd.read_excel(BytesIO(response.content))

# Extract the precinct IDs from the column (assumed to be named "Precinct")
# Convert the IDs to string and strip any whitespace
precinct_ids = df['Precinct'].astype(str).str.strip().tolist()

# Modify each precinct ID by prepending '06085-00'
precincts = [f"06085-000{pid}" for pid in precinct_ids]

# Output the resulting list
# print("precincts =", precincts)

# Load the data
gdf = gpd.read_file(r"C:\Users\Chen\Downloads\CA-precincts-with-results.geojson")

# Filter precincts by gdf['GEOID']
gdf = gdf[gdf['GEOID'].isin(precincts)]

# Define the bbox for San Jose
bbox = (-122.0460405, 37.1231596, -121.5858438, 37.4691477)

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

plt.savefig('sanjose_city_election_2024.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()

sum_votes_dem = gdf['votes_dem'].sum()
sum_votes_rep = gdf['votes_rep'].sum()
sum_votes_third_party = gdf['votes_total'].sum() - sum_votes_dem - sum_votes_rep
sum_votes_total = gdf['votes_total'].sum()
print(f"Democratic % for San Jose: {100 * sum_votes_dem/sum_votes_total:.2f}%")
print(f"Republican % for San Jose: {100 * sum_votes_rep/sum_votes_total:.2f}%")
print(f"Third Party % for San Jose: {100 * sum_votes_third_party/sum_votes_total:.2f}%")
