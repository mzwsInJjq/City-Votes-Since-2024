import csv
from collections import defaultdict

def calculate_votes_by_city(file_path):
    """
    Calculate Democratic, Republican, and Third Party vote percentages by city/town in King County.
    Cities are identified by the first part of precinct names (before the first space).
    """
    # Dictionary to store votes by city
    city_votes = defaultdict(lambda: {'democratic': 0, 'republican': 0, 'third_party': 0})
    
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Only process rows for President and Vice President race
            if row['Race'] != 'President and Vice President of the United States President and Vice President of the United States':
                continue
            
            # Extract city code from precinct name (first part before space)
            precinct = row['Precinct']
            if not precinct or ' ' not in precinct:
                continue
            
            city_code = precinct.split(' ')[0]
            vote_count = int(row['SumOfCount']) if row['SumOfCount'].isdigit() else 0
            
            # Categorize votes by candidate
            counter_type = row['CounterType']
            
            if counter_type == 'Kamala D. Harris / Tim Walz':
                city_votes[city_code]['democratic'] += vote_count
            elif counter_type == 'Donald J. Trump / JD Vance':
                city_votes[city_code]['republican'] += vote_count
            elif (counter_type != 'Kamala D. Harris / Tim Walz' and 
                  counter_type != 'Donald J. Trump / JD Vance' and 
                  not counter_type.startswith('Times ') and 
                  counter_type != 'Registered Voters'):
                city_votes[city_code]['third_party'] += vote_count
    
    # Calculate percentages and prepare results
    city_results = []
    
    for city_code, votes in city_votes.items():
        total_votes = votes['democratic'] + votes['republican'] + votes['third_party']
        
        if total_votes == 0:
            continue
        
        dem_percentage = (votes['democratic'] / total_votes) * 100
        rep_percentage = (votes['republican'] / total_votes) * 100
        third_percentage = (votes['third_party'] / total_votes) * 100
        
        city_results.append({
            'city': city_code,
            'dem_pct': dem_percentage,
            'rep_pct': rep_percentage,
            'third_pct': third_percentage,
            'total_votes': total_votes
        })
    
    # Sort by Democratic percentage (highest to lowest)
    city_results.sort(key=lambda x: x['dem_pct'], reverse=True)
    
    return city_results

def print_results(city_results):
    """Print results in the requested compact format."""
    print("Vote Percentages by City/Town in King County (sorted by Democratic %)")
    print("=" * 70)
    
    for i, result in enumerate(city_results, 1):
        print(f"{i:2d}. {result['city']:4s} D: {result['dem_pct']:7.5f}% "
              f"R: {result['rep_pct']:7.5f}% T: {result['third_pct']:7.5f}%")

def main():
    file_path = r'C:\Users\Chen\Downloads\final-results-report.csv'
    
    try:
        city_results = calculate_votes_by_city(file_path)
        print_results(city_results)
        
        print(f"\nTotal cities/towns analyzed: {len(city_results)}")
        
        # Optional: Show some summary statistics
        if city_results:
            highest_dem = city_results[0]
            lowest_dem = city_results[-1]
            print(f"\nHighest Democratic %: {highest_dem['city']} ({highest_dem['dem_pct']:.5f}%)")
            print(f"Lowest Democratic %: {lowest_dem['city']} ({lowest_dem['dem_pct']:.5f}%)")
            
    except FileNotFoundError:
        print(f"Error: Could not find the file at {file_path}")
        print("Please ensure the CSV file exists at the specified location.")
    except Exception as e:
        print(f"Error processing the file: {e}")

if __name__ == "__main__":
    main()
