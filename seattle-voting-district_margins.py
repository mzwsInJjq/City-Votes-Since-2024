# Data Source1: https://cdn.kingcounty.gov/-/media/king-county/depts/elections/results/2024/11/final-results-report.csv
# Data Source2: https://gis-kingcounty.opendata.arcgis.com/datasets/a9bcf8b7e83a402aaf68479c244b3131_418/

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import csv
from math import inf

# Function to calculate voting percentages for each precinct
def calculate_voting_percentages(file_path):
    precinct_votes = {}
    
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not row['Precinct'].startswith('SEA ') or row['Race'] != 'President and Vice President of the United States President and Vice President of the United States':
                continue
            precinct = row['Precinct']
            if precinct not in precinct_votes:
                precinct_votes[precinct] = {'democratic': 0, 'republican': 0, 'third_party': 0}
            if row['CounterType'] == 'Kamala D. Harris / Tim Walz':
                precinct_votes[precinct]['democratic'] += int(row['SumOfCount'])
            elif row['CounterType'] == 'Donald J. Trump / JD Vance':
                precinct_votes[precinct]['republican'] += int(row['SumOfCount'])
            elif row['CounterType'] != 'Kamala D. Harris / Tim Walz' and row['CounterType'] != 'Donald J. Trump / JD Vance' and not row['CounterType'].startswith('Times ') and row['CounterType'] != 'Registered Voters':
                precinct_votes[precinct]['third_party'] += int(row['SumOfCount'])
    
    for precinct, votes in precinct_votes.items():
        total_votes = votes['democratic'] + votes['republican'] + votes['third_party']
        if total_votes > 0:
            votes['democratic_percentage'] = (votes['democratic'] / total_votes) * 100
            votes['republican_percentage'] = (votes['republican'] / total_votes) * 100
            votes['third_party_percentage'] = (votes['third_party'] / total_votes) * 100
        else:
            votes['democratic_percentage'] = -inf
            votes['republican_percentage'] = 0
            votes['third_party_percentage'] = 0
    
    return precinct_votes

# Function to map margins to colors
def get_margin_color(democratic_percentage, republican_percentage):
    margin = democratic_percentage - republican_percentage
    if margin <= -100:
        return '#FFFFFF'  # No data (white)
    elif margin >= 90:
        return '#000099'  # Darkest blue
    elif margin >= 80:
        return '#0000CC'
    elif margin >= 70:
        return '#0000FF'
    elif margin >= 60:
        return '#3333FF'
    elif margin >= 50:
        return '#6666FF'
    elif margin >= 40:
        return '#7F7FFF'
    elif margin >= 30:
        return '#9999FF'
    elif margin >= 20:
        return '#B2B2FF'
    elif margin >= 10:
        return '#CCCCFF'
    elif margin >= 0:
        return '#E6E6FF'  # Lightest blue
    elif margin >= -10:
        return '#FFE6E6'  # Lightest red
    elif margin >= -20:
        return '#FFCCCC'
    elif margin >= -30:
        return '#FFB2B2'
    elif margin >= -40:
        return '#FF9999'
    elif margin >= -50:
        return '#FF7F7F'
    elif margin >= -60:
        return '#FF6666'
    elif margin >= -70:
        return '#FF3333'
    elif margin >= -80:
        return '#FF0000'
    elif margin >= -90:
        return '#CC0000'
    else:
        return '#990000'  # Darkest red

# Load the shapefile
shapefile_path = r'C:\Users\Chen\Downloads\Voting_Districts_of_King_County___votdst_area\Voting_Districts_of_King_County___votdst_area.shp'
gdf = gpd.read_file(shapefile_path)

# Filter districts that start with 'SEA '
filtered_gdf = gdf[gdf['NAME'].str.startswith('SEA ')]

# Calculate voting percentages
file_path = r'C:\Users\Chen\Downloads\final-results-report.csv'
precinct_votes = calculate_voting_percentages(file_path)

# Map colors to precincts based on margins
filtered_gdf['color'] = filtered_gdf['NAME'].apply(lambda x: get_margin_color(precinct_votes[x]['democratic_percentage'], precinct_votes[x]['republican_percentage']) if x in precinct_votes else '#FFFFFF')

# Plot the filtered shapefile with colors
fig, ax = plt.subplots(figsize=(12, 12))  # Increase figure size
filtered_gdf.plot(ax=ax, color=filtered_gdf['color'], edgecolor='white', linewidth=0.075)
plt.title('Seattle Voting Districts - 2024 Presidential Election Margins')
ax.axis('off')

# Create a color gradient bar
cmap = mcolors.ListedColormap([
    '#990000', '#CC0000', '#FF0000', '#FF3333', '#FF6666', '#FF7F7F', '#FF9999', '#FFB2B2', '#FFCCCC', '#FFE6E6',
    '#E6E6FF', '#CCCCFF', '#B2B2FF', '#9999FF', '#7F7FFF', '#6666FF', '#3333FF', '#0000FF', '#0000CC', '#000099'
])
norm = mcolors.BoundaryNorm(range(-100, 101, 10), cmap.N)

# Add color bar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.0125, pad=0.02, aspect=40)
cbar.set_ticks(range(-100, 101, 10))
cbar.ax.tick_params(labelsize=8)
cbar.set_ticklabels([str(x) for x in range(-100, 101, 10)])
cbar.set_label('Democratic Margin %')

# Save the plot as a vector PDF
plt.savefig('seattle_voting_districts_margins_2024.pdf', format='pdf', bbox_inches='tight')
plt.show()

# Print the name of the precinct with the highest/lowest Democratic margin
max_margin_precinct = max(precinct_votes, key=lambda x: precinct_votes[x]['democratic_percentage'] - precinct_votes[x]['republican_percentage'])
min_margin_precinct = min(precinct_votes, key=lambda x: precinct_votes[x]['democratic_percentage'] - precinct_votes[x]['republican_percentage'] if precinct_votes[x]['democratic_percentage'] - precinct_votes[x]['republican_percentage'] > -100 else inf)
print(f'Total Votes in {max_margin_precinct}: {int(sum(precinct_votes[max_margin_precinct].values()))} ({precinct_votes[max_margin_precinct]["democratic_percentage"]:.2f}% - {precinct_votes[max_margin_precinct]["republican_percentage"]:.2f}%)')
print(f'Total Votes in {min_margin_precinct}: {int(sum(precinct_votes[min_margin_precinct].values()))} ({precinct_votes[min_margin_precinct]["democratic_percentage"]:.2f}% - {precinct_votes[min_margin_precinct]["republican_percentage"]:.2f}%)')