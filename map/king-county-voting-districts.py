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
            if row['Race'] != 'President and Vice President of the United States President and Vice President of the United States':
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

# Load the shapefile
shapefile_path = r'C:\Users\Chen\Downloads\Voting_Districts_of_King_County___votdst_area\Voting_Districts_of_King_County___votdst_area.shp'
gdf = gpd.read_file(shapefile_path)

# Calculate voting percentages
file_path = r'C:\Users\Chen\Downloads\final-results-report.csv'
precinct_votes = calculate_voting_percentages(file_path)

# Map colors to precincts
gdf['color'] = gdf['NAME'].apply(lambda x: get_color(precinct_votes[x]['democratic_percentage']) if x in precinct_votes else '#FFFFFF')

# Plot the shapefile with colors
fig, ax = plt.subplots(figsize=(12, 12))  # Increase figure size
gdf.plot(ax=ax, color=gdf['color'], edgecolor='black', linewidth=0.2)  # Thinner boundaries
plt.title('King County Voting Districts - 2024 Presidential Election Results')
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
plt.savefig('king_county_voting_districts_2024.pdf', format='pdf', bbox_inches='tight')

# plt.show()