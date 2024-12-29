# Data Source1: https://vote.nyc/page/election-results-summary
# Data Source2: https://data.cityofnewyork.us/City-Government/Election-Districts/h2n3-98hq

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import csv

# Function to calculate voting percentages for each precinct
def calculate_voting_percentages(file_path):
    precinct_votes = {}
    
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                tally = int(row['Tally'])
            except ValueError:
                tally = int(''.join(row['Tally'].split(',')))  # Remove commas and convert to integer
            precinct = float(row['AD'] + row['ED'])  # Prepend "23" and convert to float
            if precinct not in precinct_votes:
                precinct_votes[precinct] = {'democratic': 0, 'republican': 0, 'third_party': 0}
            if row['Unit Name'] in ['Kamala D. Harris / Tim Walz (Democratic)', 'Kamala D. Harris / Tim Walz (Working Families)']:
                precinct_votes[precinct]['democratic'] += tally
            elif row['Unit Name'] in ['Donald J. Trump / JD Vance (Republican)', 'Donald J. Trump / JD Vance (Conservative)']:
                precinct_votes[precinct]['republican'] += tally
            elif row['Unit Name'] == 'Scattered':
                precinct_votes[precinct]['third_party'] += tally
    
    for precinct, votes in precinct_votes.items():
        total_votes = votes['democratic'] + votes['republican'] + votes['third_party']
        if total_votes > 0:
            votes['democratic_percentage'] = (votes['democratic'] / total_votes) * 100
            votes['republican_percentage'] = (votes['republican'] / total_votes) * 100
            votes['third_party_percentage'] = (votes['third_party'] / total_votes) * 100
        else:
            votes['democratic_percentage'] = -1
            votes['republican_percentage'] = 0
            votes['third_party_percentage'] = 0
    
    return precinct_votes

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

# Load the NYC shapefile
shapefile_path = r'C:\Users\Chen\Downloads\nyed_20241229\geo_export_9a0d6a75-2e8c-4fca-985e-dfbe56bc57d4.shp'
gdf = gpd.read_file(shapefile_path)

# Print column names to identify the correct column for precincts
print(gdf.columns)

# Print out some district names
print(gdf.head())

# Calculate voting percentages
file_path = r'C:\Users\Chen\Downloads\00000100000Citywide President Vice President Citywide EDLevel.csv'
precinct_votes = calculate_voting_percentages(file_path)

# Debug print to check precinct_votes
print("Precinct Votes:", precinct_votes)

# Assuming the correct column name is 'elect_dist' (adjust if necessary)
gdf['color'] = gdf['elect_dist'].apply(lambda x: get_color(precinct_votes[float(x)]['democratic_percentage']) if float(x) in precinct_votes else '#FFFFFF')

# Debug print to check colors assigned
print("Colors assigned:", gdf['color'].unique())

# Plot the shapefile with colors
fig, ax = plt.subplots(figsize=(12, 12))  # Increase figure size
gdf.plot(ax=ax, color=gdf['color'], edgecolor='black', linewidth=0.2)  # Thinner boundaries
plt.title('NYC Voting Districts - 2024 Presidential Election Results')
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

# Save the plot as a vector PDF
plt.savefig('nyc_voting_districts_2024.pdf', format='pdf', bbox_inches='tight')

plt.show()