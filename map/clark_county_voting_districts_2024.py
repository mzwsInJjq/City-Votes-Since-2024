# Data Source1: https://www.nvsos.gov/electionresults/PrecinctReport.aspx
# Data Source2: https://mapsrv.clarkcountynv.gov/pub/crel/crel-shp.zip

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors

# Load the shapefile
shapefile_path = r'C:\Users\Chen\Downloads\las-vegas-crel-shp\precinct_p.shp'
gdf = gpd.read_file(shapefile_path)

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
plt.title('Clark County Voting Districts - 2024 Presidential Election Results')
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
plt.savefig('clark_county_voting_districts_2024.pdf', format='pdf', bbox_inches='tight')
plt.show()