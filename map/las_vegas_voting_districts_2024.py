# Data Source1: https://www.nvsos.gov/electionresults/PrecinctReport.aspx
# Data Source2: https://mapsrv.clarkcountynv.gov/pub/crel/crel-shp.zip

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors

las_vegas_precincts = [2003, 2004, 2005, 2009, 2011, 2013, 2014, 2015, 2020, 2021, 2023, 2025, 2028, 2029, 2030, 2032, 2033, 2036, 2037, 2046, 2051, 2053, 2054, 2055, 2056, 2063, 2065, 2067, 2072, 2073, 2079, 2081, 2082, 2352, 2600, 2605, 2611, 2614, 2622, 2633, 2641, 2643, 2651, 2654, 2662, 2663, 2682, 2695, 2696, 2700, 2706, 2709, 2710, 2711, 3000, 3003, 3007, 3009, 3011, 3013, 3014, 3016, 3017, 3018, 3021, 3022, 3027, 3036, 3037, 3038, 3039, 3040, 3043, 3045, 3055, 3056, 3058, 3059, 3061, 3062, 3065, 3066, 3068, 3069, 3072, 3074, 3217, 3361, 3363, 3364, 3366, 3370, 3373, 3374, 3382, 3383, 3385, 3391, 3392, 3414, 3417, 3418, 3435, 3464, 3544, 3546, 3547, 3557, 3565, 3576, 3583, 3587, 3588, 3602, 3604, 3606, 3607, 3613, 3700, 3705, 3706, 3709, 3714, 3716, 3717, 3719, 3724, 3727, 3729, 3730, 3732, 3740, 3747, 3748, 3750, 3753, 3754, 3755, 3762, 3763, 3764, 3765, 3766, 3769, 3771, 3773, 3780, 3781, 3786, 3787, 3793, 3800, 3863, 4000, 4001, 4007, 4008, 4009, 4019, 4020, 4026, 4027, 4028, 4030, 4032, 4034, 4040, 4387, 4461, 4463, 4510, 4526, 4528, 4529, 4540, 4541, 4543, 4547, 4548, 4605, 4612, 4613, 4615, 4623, 4633, 4638, 5001, 5002, 5003, 5005, 5007, 5012, 5018, 5022, 5028, 5030, 5031, 5044, 5350, 5384, 5533, 5542, 5545, 5554, 5563, 5565, 6007, 6625, 6632, 6711]

# Load the shapefile
shapefile_path = r'C:\Users\Chen\Downloads\las-vegas-crel-shp\precinct_p.shp'
gdf = gpd.read_file(shapefile_path)
gdf = gdf[gdf['PREC'].isin(las_vegas_precincts)]

# Load the CSV file
csv_path = r'C:\Users\Chen\Downloads\2024StatewideGeneralElectionResultsClark.csv'
df = pd.read_csv(csv_path)

# Replace asterisks with zeros
df['Votes'] = df['Votes'].replace('*', '0')

# Filter for Harris and Trump votes
df = df[df['Race'] == 'President and Vice President of the United States']
df = df[df['Candidate'].isin(['Harris, Kamala D. and Walz, Tim', 'Trump, Donald J. and Vance, JD'])]

# Pivot the data to get votes for each candidate in separate columns
df_pivot = df.pivot_table(index='Precinct', columns='Candidate', values='Votes', aggfunc='sum').reset_index()
df_pivot.columns = ['Precinct', 'Harris Votes', 'Trump Votes']

# Convert votes to numeric, handling non-numeric values
df_pivot['Harris Votes'] = pd.to_numeric(df_pivot['Harris Votes'], errors='coerce').fillna(0).astype(int)
df_pivot['Trump Votes'] = pd.to_numeric(df_pivot['Trump Votes'], errors='coerce').fillna(0).astype(int)

# Calculate total votes and Democratic percentage
df_pivot['Total Votes'] = df_pivot['Harris Votes'] + df_pivot['Trump Votes']
df_pivot['Democratic %'] = (df_pivot['Harris Votes'] / df_pivot['Total Votes']) * 100

# Merge the GeoDataFrame with the DataFrame
merged_gdf = gdf.merge(df_pivot, left_on='PREC', right_on='Precinct')

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
plt.title('Las Vegas Voting Districts - 2024 Presidential Election Results')
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
plt.savefig('las_vegas_voting_districts_2024.pdf', format='pdf', bbox_inches='tight')
plt.show()

# Calculate Las Vegas's citywide Democratic/Republican vote percentages
df_pivot = df_pivot[df_pivot['Precinct'].isin(las_vegas_precincts)]
total_dem_votes = df_pivot['Harris Votes'].sum()
total_rep_votes = df_pivot['Trump Votes'].sum()
total_votes = total_dem_votes + total_rep_votes

citywide_dem_percentage = (total_dem_votes / total_votes) * 100
citywide_rep_percentage = (total_rep_votes / total_votes) * 100

# Print the votes and percentages
print("Citywide Democratic Votes:", total_dem_votes, "(", citywide_dem_percentage, "%)")
print("Citywide Republican Votes:", total_rep_votes, "(", citywide_rep_percentage, "%)")