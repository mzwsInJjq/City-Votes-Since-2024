# Data Source1: https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Ward-Precincts-2023-/6piy-vbxa/about_data
# Data Source2: https://chicagoelections.gov/elections/results/41

import re
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors

# Load the shapefile
shapefile_path = r'C:\Users\Chen\Downloads\Boundaries - Ward Precincts (2023-)_20241230\geo_export_b67411d2-efd1-4839-aa34-47786a1a3107.shp'
gdf = gpd.read_file(shapefile_path)

# Print column names to identify the correct column for precincts
print("Columns in shapefile:", gdf.columns)

# Output the first 5 rows to debug
print("First 5 rows of the shapefile:")
print(gdf.head())

# Load the CSV file
csv_path = r'C:\Users\Chen\Downloads\chicago.csv'

# Read the CSV file
with open(csv_path, 'r') as file:
    lines = file.readlines()

# Initialize variables
data = []
current_ward = None

# Parse the CSV file
for line in lines:
    line = line.strip()
    if line.startswith('Ward'):
        current_ward = line
    elif line and not line.startswith('Precinct') and line[0].isdigit():
        parts = line.split(',')
        if len(parts) == 8:
            precinct, total_voters, dem_votes, dem_pct, rep_votes, rep_pct, third_votes, third_pct = parts
            data.append([float(re.sub("[^0-9]", "", current_ward)), float(precinct), int(total_voters), int(dem_votes), float(dem_pct.strip('%')), int(rep_votes), float(rep_pct.strip('%')), int(third_votes), float(third_pct.strip('%'))])

# Create a DataFrame
columns = ['Ward', 'Precinct', 'Total Voters', 'Democratic Votes', 'Democratic %', 'Republican Votes', 'Republican %', 'Third Party Votes', 'Third Party %']
df = pd.DataFrame(data, columns=columns)

# Print the DataFrame to verify
print(df.head(50))

#If for any column, 'Total Voters'is 0, set 'Democratic Votes' to -1
df.loc[df['Total Voters'] == 0, 'Democratic Votes'] = -1

# Merge the GeoDataFrame with the DataFrame
merged_gdf = gdf.merge(df, left_on=['ward', 'precinct'], right_on=['Ward', 'Precinct'])

# Function to map percentages to colors
def get_color(democratic_percentage):
    if democratic_percentage >= 90:
        return '#0000FF'  # Deep blue
    elif democratic_percentage >= 80:
        return '#3333FF'
    elif democratic_percentage >= 70:
        return '#6666FF'
    elif democratic_percentage >= 60:
        return '#9999FF'
    elif democratic_percentage >= 50:
        return '#CCCCFF'
    elif democratic_percentage >= 40:
        return '#FFCCCC'
    elif democratic_percentage >= 30:
        return '#FF9999'
    elif democratic_percentage >= 20:
        return '#FF6666'
    elif democratic_percentage >= 10:
        return '#FF3333'
    elif democratic_percentage >= 0:
        return '#FF0000'  # Deep red
    else:
        return '#FFFFFF'  # White

# Apply colors
merged_gdf['color'] = merged_gdf['Democratic %'].apply(get_color)

# Plot the precincts with Democratic Vote %
fig, ax = plt.subplots(figsize=(12, 12))
merged_gdf.plot(ax=ax, color=merged_gdf['color'], edgecolor='black', linewidth=0.2)
plt.title('Chicago Voting Districts - 2024 Presidential Election Results')
ax.axis('off')

# Create a color gradient bar
cmap = mcolors.ListedColormap(['#FF0000', '#FF3333', '#FF6666', '#FF9999', '#FFCCCC', '#CCCCFF', '#9999FF', '#6666FF', '#3333FF', '#0000FF'])
norm = mcolors.BoundaryNorm([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], cmap.N)

# Add color bar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.02, pad=0.02)
cbar.set_ticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])  # Add small ticks
cbar.set_ticklabels(['0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'])  # Set tick labels
cbar.set_label('Democratic Vote %')

# Save the plot
plt.savefig('chicago_voting_districts_2024.pdf', format='pdf', bbox_inches='tight')
plt.show()
