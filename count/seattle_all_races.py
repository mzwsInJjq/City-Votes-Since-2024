import csv
from collections import defaultdict

def analyze_seattle_votes(file_path):
    """
    Analyze how Seattle voted in every race.
    Seattle precincts are identified by starting with 'SEA ' (with space).
    """
    race_votes = defaultdict(lambda: defaultdict(int))
    
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Filter for Seattle precincts only (starts with 'SEA ')
            if not row['Precinct'].startswith('SEA '):
                continue
            
            race = row['Race']
            counter_type = row['CounterType']
            vote_count = int(row['SumOfCount']) if row['SumOfCount'].isdigit() else 0
            
            # Skip registration and timing entries
            if (counter_type.startswith('Times ') or 
                counter_type == 'Registered Voters' or
                vote_count == 0):
                continue
            
            race_votes[race][counter_type] += vote_count
    
    return race_votes

def print_race_results(race_votes):
    """Print compact results for each race."""
    print("Seattle Voting Results by Race")
    print("=" * 80)
    
    race_number = 1
    for race, candidates in race_votes.items():
        # Calculate total votes for this race
        total_votes = sum(candidates.values())
        
        if total_votes == 0:
            continue
        
        print(f"\n{race_number}. {race}")
        print("-" * min(len(race) + len(str(race_number)) + 2, 80))

        # Sort candidates by vote count (highest first)
        sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        
        for i, (candidate, votes) in enumerate(sorted_candidates, 1):
            percentage = (votes / total_votes) * 100
            print(f"   {i:2d}. {candidate:40s} {votes:6,} ({percentage:6.2f}%)")
        
        print(f"   Total votes: {total_votes:,}")
        race_number += 1

def print_summary_stats(race_votes):
    """Print summary statistics."""
    total_races = len(race_votes)
    total_votes_all_races = sum(sum(candidates.values()) for candidates in race_votes.values())
    
    print(f"\nSummary:")
    print(f"Total races: {total_races}")
    print(f"Total votes cast across all races: {total_votes_all_races:,}")

def main():
    file_path = r'C:\Users\Chen\Downloads\final-results-report.csv'
    
    try:
        race_votes = analyze_seattle_votes(file_path)
        
        if not race_votes:
            print("No Seattle voting data found. Check if precincts start with 'SEA ' in the CSV file.")
            return
        
        print_race_results(race_votes)
        print_summary_stats(race_votes)
        
    except FileNotFoundError:
        print(f"Error: Could not find the file at {file_path}")
        print("Please ensure the CSV file exists at the specified location.")
    except Exception as e:
        print(f"Error processing the file: {e}")

if __name__ == "__main__":
    main()
