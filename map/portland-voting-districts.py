# Data Source1: https://multco.us/file/multnomah_elections_precinct_split_2024/download
# Data Source2: https://multco.us/file/sovc2_-_election20241105general.csv/download
# Data Source3: https://www.portland.gov/elections/maps-and-data-city-portland

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import csv

# List of Portland precincts you want to plot
portland_precincts = ['4101', '4102', '4103', '4104', '4105', '4701', '4702',
 '4703', '4704', '4705', '4706', '4707', '4708', '4709', '4710',
 '4201', '4202', '4203', '4204', '4205', '4206', '4207', '4208',
 '4801', '4802', '4803', '4804', '4805', '4806', '4809', '4301',
 '4302', '4303', '4304', '4305', '4306', '4307', '3803', '3804',
 '3805', '3806', '3301', '3302', '3303', '3304', '3305', '3306',
 '3307', '3308', '2801', '2803', '2804', '2805', '2806', '4910',
 '4401', '4402', '4403', '4404', '4405', '4406', '4407', '3401',
 '5001', '5003', '4501', '4502', '4503', '4505', '4506', '4507',
 '4508', '4509', '4601', '4602', '4603', '4604', '4605', '4606',
 '4607']
portland_precincts.remove('3301')

# 1. Load the Portland precinct shapefile
shapefile_path = r'C:\Users\Chen\Downloads\Multnomah_Elections_Precinct_Split_2024\Multnomah_Elections_Precinct_Split_2024.shp'
gdf = gpd.read_file(shapefile_path)

# Filter the GeoDataFrame to include only Portland precincts
filtered_gdf = gdf[gdf['Precinct'].isin(portland_precincts)]

# 2. Define a function to parse the CSV and collect vote counts
def parse_election_csv(csv_path):
    precinct_votes = {}  # {precinct: {"dem": 0, "gop": 0, "other": 0}}

    with open(csv_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            contest = row["Contest"]
            choice = row["Choice"]
            precinct = row["Precinct"]
            votes_str = row["Votes"]

            # Skip rows that don't match the contest of interest
            if contest != "President and Vice President (VGNone) (Vote for 1)":
                continue
            
            # Clean precinct (int) and votes (remove commas)
            try:
                precinct_int = int(precinct)
                votes = int(votes_str.replace(",", ""))
            except ValueError:
                continue

            if precinct_int not in precinct_votes:
                precinct_votes[precinct_int] = {"dem": 0, "gop": 0, "other": 0}

            # Tally votes
            if choice == "Kamala D Harris/Tim Walz":
                precinct_votes[precinct_int]["dem"] += votes
            elif choice == "Donald J Trump/JD Vance":
                precinct_votes[precinct_int]["gop"] += votes
            else:
                precinct_votes[precinct_int]["other"] += votes
    
    return precinct_votes

# 3. Parse the CSV
csv_path = r'C:\Users\Chen\Downloads\SOVC2 - election20241105General.csv.csv'
precinct_votes = parse_election_csv(csv_path)

# 4. Add columns for total votes and percentages
vote_data = []
for prec, counts in precinct_votes.items():
    dem = counts["dem"]
    gop = counts["gop"]
    other = counts["other"]
    total = dem + gop + other
    if total > 0:
        dem_pct = (dem / total) * 100
        gop_pct = (gop / total) * 100
        other_pct = (other / total) * 100
    else:
        dem_pct = -1
        gop_pct = 0
        other_pct = 0
    vote_data.append([prec, dem, gop, other, total, dem_pct, gop_pct, other_pct])

df_cols = ["Precinct", "Dem Votes", "GOP Votes", "Other Votes", "Total Votes",
           "Dem %", "GOP %", "Other %"]
votes_df = pd.DataFrame(vote_data, columns=df_cols)

# Print the first 5 rows of the votes_df DataFrame
print("First 5 rows of the votes_df DataFrame:")
print(votes_df.head())

# 5. Add Dem % to filtered_gdf based on votes_df
votes_df["Precinct"] = votes_df["Precinct"].astype(str)
merged_gdf = pd.merge(filtered_gdf, votes_df, on="Precinct")

# 6. Define a function to map Democratic vote percentage to a color
def get_color(dem_perc):
    if dem_perc >= 90:
        return '#0000FF'  # Deep blue
    elif dem_perc >= 80:
        return '#3333FF'
    elif dem_perc >= 70:
        return '#6666FF'
    elif dem_perc >= 60:
        return '#9999FF'
    elif dem_perc >= 50:
        return '#CCCCFF'
    elif dem_perc >= 40:
        return '#FFCCCC'
    elif dem_perc >= 30:
        return '#FF9999'
    elif dem_perc >= 20:
        return '#FF6666'
    elif dem_perc >= 10:
        return '#FF3333'
    elif dem_perc >= 0:
        return '#FF0000'  # Deep red
    else:
        return '#FFFFFF'  # White

# Color precincts by Democratic vote percentage
merged_gdf["color"] = merged_gdf["Dem %"].apply(get_color)

# Print the first 5 rows of the merged GeoDataFrame
print("First 5 rows of the merged GeoDataFrame:")
print(merged_gdf.head())

# 7. Plot the precincts
fig, ax = plt.subplots(figsize=(12, 12))
merged_gdf.plot(ax=ax, color=merged_gdf['color'], edgecolor='black', linewidth=0.2)
plt.title('Portland Voting Districts - 2024 Presidential Election Results')
ax.axis('off')

# Create a color gradient bar
cmap = mcolors.ListedColormap([
    '#FF0000', '#FF3333', '#FF6666', '#FF9999', '#FFCCCC',
    '#CCCCFF', '#9999FF', '#6666FF', '#3333FF', '#0000FF'
])
norm = mcolors.BoundaryNorm([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], cmap.N)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', fraction=0.02, pad=0.02)
cbar.set_ticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
cbar.set_ticklabels(['0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'])
cbar.set_label('Democratic Vote %')

# 8. Save the plot
plt.savefig('portland_voting_districts_2024.pdf', format='pdf', bbox_inches='tight')
plt.show()

# 9. Calculate the total DEM, GOP, and Third Parties Votes in Portland from merged_gdf
total_dem_votes = merged_gdf["Dem Votes"].sum()
total_gop_votes = merged_gdf["GOP Votes"].sum()
total_other_votes = merged_gdf["Other Votes"].sum()

total_dem_pct = (total_dem_votes / (total_dem_votes + total_gop_votes + total_other_votes)) * 100
total_gop_pct = (total_gop_votes / (total_dem_votes + total_gop_votes + total_other_votes)) * 100
total_other_pct = (total_other_votes / (total_dem_votes + total_gop_votes + total_other_votes)) * 100

print("Total Democratic Votes:", total_dem_votes, "(", total_dem_pct, "%)")
print("Total GOP Votes:", total_gop_votes, "(", total_gop_pct, "%)")
print("Total Third Parties Votes:", total_other_votes, "(", total_other_pct, "%)")