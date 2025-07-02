# 2023 TIGER/Line +
# https://data2.nhgis.org/main

# https://kingcounty.gov/en/dept/elections/results/2025/february-special
# Seattle City Proposition Nos. 1A and 1B

import csv
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# Load the data
gdf = gpd.read_file(r"C:\Users\Chen\Downloads\WA-precincts-with-results.geojson")
df = gpd.read_file(r"C:\Users\Chen\Downloads\nhgis0001_shapefile_tl2023_us_state_2023\US_state_2023.shp")
df = df[df['STATEFP'] == '53']
df = df.to_crs("epsg:4326")

# Filter precincts by gdf['GEOID']
gdf = gdf[gdf['GEOID'].str.startswith('53033-SEA ')]

# Define the bbox for Seattle
bbox = (-122.4596960, 47.4810022, -122.2244330, 47.7341503)

# Filter the GeoDataFrame to include only precincts within the bbox
gdf = gdf.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]

# Create a color map
norm = TwoSlopeNorm(vmin=-100, vcenter=0, vmax=100)
cmap = plt.get_cmap('seismic_r')  # '_r' reverses the color map

# Initialize vote counts
total_votes = 0
a_votes = 0
b_votes = 0

def calculate_voting_percentage(file_path):
    global a_votes, b_votes, total_votes
    # Read the CSV file
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Race'] != 'City of Seattle Proposition Nos. 1A and 1B (continued)':
                continue
            lookup_key = '53033-' + row['Precinct']
            # print(f"Trying lookup_key: {lookup_key}")
            if row['CounterType'] == 'Proposition 1A':
                a_votes += int(row['SumOfCount'])
                # Update the GeoDataFrame with the vote count for Proposition 1A
                if lookup_key in gdf['GEOID'].values:
                    gdf.loc[gdf['GEOID'] == lookup_key, 'Proposition 1A'] = int(row['SumOfCount'])
                else:
                    print(f"Warning: {lookup_key} not found in GEOID column.")
            if row['CounterType'] == 'Proposition 1B':
                b_votes += int(row['SumOfCount'])
                # Update the GeoDataFrame with the vote count for Proposition 1B
                if lookup_key in gdf['GEOID'].values:
                    gdf.loc[gdf['GEOID'] == lookup_key, 'Proposition 1B'] = int(row['SumOfCount'])
                else:
                    print(f"Warning: {lookup_key} not found in GEOID column.")


    total_votes = a_votes + b_votes
    a_percentage = (a_votes / total_votes) * 100
    b_percentage = (b_votes / total_votes) * 100
    return a_percentage, b_percentage

file_path = r'D:\Misc\king-county-feb-2025-special-election-final-results-report.csv'
a_percentage, b_percentage = calculate_voting_percentage(file_path)

# Calculate the percentage lead for Proposition 1A over Proposition 1B
gdf['pct_a_lead'] = (gdf['Proposition 1A'] - gdf['Proposition 1B']) / (gdf['Proposition 1A'] + gdf['Proposition 1B']) * 100

print("City of Seattle Proposition Nos. 1A and 1B")
print(f"Total votes: {total_votes}")

print(f"Proposition 1A: {a_votes}")
print(f"Proposition 1A %: {a_percentage}%")

print(f"Proposition 1B: {b_votes}")
print(f"Proposition 1B %: {b_percentage}%")

# Clip the GeoDataFrame to the state boundaries (for coastline)
gdf = gpd.overlay(gdf, df, how='intersection', keep_geom_type=False)

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
gdf.plot(column='pct_a_lead', cmap=cmap, linewidth=0, ax=ax, norm=norm)

# Set the axis limits to match the bounding box
ax.set_xlim(bbox[0], bbox[2])
ax.set_ylim(bbox[1], bbox[3])

# Remove axis
ax.axis('off')

plt.title('Seattle City Proposition Nos. 1A and 1B', fontsize=20)
plt.savefig('seattle_city_special_election_feb_2025.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()
