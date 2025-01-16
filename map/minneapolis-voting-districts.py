import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import csv

# Load the Minneapolis shapefile
shapefile_path = r'C:\Users\Chen\Downloads\Minneapolis_Election_Precincts\Election_Precincts.shp'
gdf = gpd.read_file(shapefile_path)

# Extract Minneapolis ward-precinct pairs and their corresponding precinct IDs
def extract_ward_precinct_pairs(file_path):
    ward_precinct_pairs = {}
    
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if row[2].startswith('MINNEAPOLIS'):
                precinct_id = row[1].zfill(4)  # Pad precinct_id to 4 digits with leading zeros
                ward_precinct = row[2].replace('MINNEAPOLIS ', '').replace('W', 'Ward').replace('-', ' ').replace(' P', ' - Precinct')
                # Remove any leading zero in ward_precinct key names e.g. 'Ward 1 - Precinct 06' to 'Ward 1 - Precinct 6'
                ward_parts = ward_precinct.split(' - Precinct ')
                if len(ward_parts) == 2:
                    precinct_num = str(int(ward_parts[1]))  # Remove leading zeros
                    ward_precinct = f"{ward_parts[0]} - Precinct {precinct_num}"
                ward_precinct_pairs[ward_precinct] = precinct_id
    
    return ward_precinct_pairs

# File path to the precinct table
precinct_table_path = r'C:\Users\Chen\Downloads\PrctTbl.txt'
ward_precinct_pairs = extract_ward_precinct_pairs(precinct_table_path)

# Invert the ward_precinct_pairs dictionary
precinct_id_to_ward_precinct = {v: k for k, v in ward_precinct_pairs.items()}

# Debug print to check ward_precinct_pairs
# print("Ward-Precinct Pairs:", ward_precinct_pairs)
# print("Precinct ID to Ward-Precinct:", precinct_id_to_ward_precinct)

# Parse the election data and calculate vote percentages
def calculate_voting_percentages(file_path, precinct_id_to_ward_precinct):
    precinct_votes = {}
    
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            if row[1] == '27':  # Filter for County ID 27
                precinct_id = row[2].zfill(4)  # Pad precinct_id to 4 digits with leading zeros
                candidate_name = row[7]
                votes = int(row[13])
                
                # Find the ward-precinct key using the precinct_id value
                ward_precinct = None

                if precinct_id in list(precinct_id_to_ward_precinct.keys()):
                    ward_precinct = precinct_id_to_ward_precinct.get(str(precinct_id))
                else:
                    continue
                
                # Debug print to check precinct_id and candidate_name
                # print(f"Processing precinct_id: {precinct_id}, ward_precinct: {ward_precinct}, candidate_name: {candidate_name}, votes: {votes}")
                
                if ward_precinct:
                    if ward_precinct not in precinct_votes:
                        precinct_votes[ward_precinct] = {'democratic': 0, 'republican': 0, 'third_party': 0}
                    
                    if candidate_name in ['Kamala D. Harris and Tim Walz']:
                        precinct_votes[ward_precinct]['democratic'] += votes
                    elif candidate_name in ['Donald J. Trump and JD Vance']:
                        precinct_votes[ward_precinct]['republican'] += votes
                    else:
                        precinct_votes[ward_precinct]['third_party'] += votes
    
    # Debug print to check vote counts before calculating percentages
    # print("Vote counts before percentages:", precinct_votes)
    
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
    
    # Debug print to check vote percentages
    # print("Vote percentages:", precinct_votes)
    
    return precinct_votes

# File path to the election data
election_data_path = r'C:\Users\Chen\Downloads\Minneapolis_USPresPct.txt'
precinct_votes = calculate_voting_percentages(election_data_path, precinct_id_to_ward_precinct)

# Debug print to check precinct_votes
# print("Precinct Votes:", precinct_votes)

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

# Adjust the WARDS_PREC format to match the ward-precinct pairs
gdf['WARDS_PREC'] = gdf.apply(lambda row: f"Ward {row['WARDS']} - Precinct {int(row['PRECINCTS'])}", axis=1)

# Assuming the correct column name is 'precinct_id' (adjust if necessary)
gdf['color'] = gdf['WARDS_PREC'].apply(lambda x: get_color(precinct_votes[x]['democratic_percentage']) if x in precinct_votes else '#FFFFFF')


# Plot the shapefile with colors
fig, ax = plt.subplots(figsize=(12, 12))  # Increase figure size
gdf.plot(ax=ax, color=gdf['color'], edgecolor='black', linewidth=0.2)  # Thinner boundaries
plt.title('Minneapolis Voting Districts - 2024 Presidential Election Results')
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
plt.savefig('minneapolis_voting_districts_2024.pdf', format='pdf', bbox_inches='tight')

plt.show()

def print_citywide_totals(precinct_votes):
    total_dem = 0
    total_gop = 0
    total_third = 0
    
    for precinct, votes in precinct_votes.items():
        total_dem += votes['democratic']
        total_gop += votes['republican']
        total_third += votes['third_party']
    
    total_votes = total_dem + total_gop + total_third
    
    print(f"\nCitywide Vote Totals:")
    print(f"Democratic: {total_dem:,} ({total_dem/total_votes*100:.2f}%)")
    print(f"Republican: {total_gop:,} ({total_gop/total_votes*100:.2f}%)")
    print(f"Third Party: {total_third:,} ({total_third/total_votes*100:.2f}%)")
    print(f"Total Votes: {total_votes:,}")

# Add after calculating precinct_votes
print_citywide_totals(precinct_votes)