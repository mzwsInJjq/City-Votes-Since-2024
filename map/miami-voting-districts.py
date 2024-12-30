import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd

# Data Source1: https://gis-mdc.opendata.arcgis.com/datasets/6dc0c7674b064d5ca5aa73330860fb29_0/explore
# Data Source2: https://www.miamidade.gov/elections/library/reports/city-of-miami-district.pdf
# Data Source3: https://enr.electionsfl.org/DAD/3713/Reports/

# Load Miami districts list
miami_districts = [501, 502, 503, 504, 505, 506, 507, 508, 
509, 510, 511, 512, 513, 514, 515, 516, 517, 
518, 519, 520, 521, 522, 523, 524, 525, 526, 
527, 528, 529, 530, 531, 532, 533, 534, 535, 
536, 537, 538, 539, 540, 541, 542, 543, 544, 
545, 546, 547, 548, 549, 550, 551, 552, 553, 
554, 556, 557, 558, 559, 560, 561, 562, 563, 
564, 565, 566, 567, 568, 569, 570, 571, 572, 
573, 574, 575, 576, 577, 578, 579, 580, 581, 
582, 583, 584, 585, 586, 587, 588, 589, 591, 
593, 595, 596, 597, 598, 599, 600, 602, 603, 
609, 610, 619, 620, 622, 624, 626, 629, 634, 
639, 645, 654, 655, 657, 661, 662, 663, 664, 
665, 669, 670, 671, 690, 698, 971, 975, 976, 
980, 981, 982, 983, 984, 985, 986, 988]

# Load election results
csv_path = r'C:\Users\Chen\Downloads\CandidateResultsbyPrecinctandParty_2024-11-15T16_43_48_1b0d490a-559f-48f7-9f2d-7b5acdf69fe1.csv'
election_df = pd.read_csv(csv_path)

# Filter for Democratic presidential votes
dem_votes = election_df[
    (election_df['Contest'] == 'President and Vice President') & 
    (election_df['Party'] == 'DEM')
].copy()

# Clean precinct numbers
dem_votes['precinct_num'] = dem_votes['Precinct Name'].str.replace('PRECINCT ', '').astype(float)

# Create precinct to percentage mapping
precinct_percentages = dict(zip(dem_votes['precinct_num'], dem_votes['% of Total Votes']))

# Load the shapefile
shapefile_path = r'C:\Users\Chen\Downloads\Precinct_gdb_-3486550073705204155\Precinct.shp'
gdf = gpd.read_file(shapefile_path)

# Print column names
print("Columns in shapefile:", gdf.columns)

# Print sample of precinct numbers
print("\nSample precincts:", gdf['ID'].head())

# Filter for Miami districts
miami_gdf = gdf[gdf['ID'].isin(miami_districts)].copy()

# Add Democratic vote percentages
miami_gdf['dem_pct'] = miami_gdf['ID'].map(precinct_percentages)

# Color mapping function
def get_color(dem_percentage):
    if pd.isna(dem_percentage):
        return '#FFFFFF'  # White for no data
    elif dem_percentage >= 80:
        return '#0000FF'  # Deep blue
    elif dem_percentage >= 70:
        return '#3333FF'
    elif dem_percentage >= 60:
        return '#6666FF'
    elif dem_percentage >= 50:
        return '#9999FF'
    elif dem_percentage >= 40:
        return '#FFCCCC'
    elif dem_percentage >= 30:
        return '#FF9999'
    elif dem_percentage >= 20:
        return '#FF6666'
    elif dem_percentage >= 10:
        return '#FF3333'
    else:
        return '#FF0000'  # Deep red

# Apply colors
miami_gdf['color'] = miami_gdf['dem_pct'].apply(get_color)

# Plot
fig, ax = plt.subplots(figsize=(12, 12))
miami_gdf.plot(ax=ax, color=miami_gdf['color'], edgecolor='black', linewidth=0.2)
plt.title('Miami Voting Districts - 2024 Presidential Election Results')
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

# Save plot
plt.savefig('miami_voting_districts_2024.pdf', format='pdf', bbox_inches='tight')
plt.show()
