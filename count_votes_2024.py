import csv

def calculate_democratic_percentage(file_path):
    global total_votes
    total_votes = 0
    global democratic_votes
    democratic_votes = 0
    global republican_votes
    republican_votes = 0
    global third_party_votes
    third_party_votes = 0

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not row['Precinct'].startswith('SEA ') or row['Race'] != 'President and Vice President of the United States President and Vice President of the United States':
                continue
            if row['CounterType'] == 'Kamala D. Harris / Tim Walz':
                democratic_votes += int(row['SumOfCount'])
            if row['CounterType'] == 'Donald J. Trump / JD Vance':
                republican_votes += int(row['SumOfCount'])
            if row['CounterType'] != 'Kamala D. Harris / Tim Walz' and row['CounterType'] != 'Donald J. Trump / JD Vance' and not row['CounterType'].startswith('Times ') and row['CounterType'] != 'Registered Voters':
                third_party_votes += int(row['SumOfCount'])
    
    total_votes = democratic_votes + republican_votes + third_party_votes
    democratic_percentage = (democratic_votes / total_votes) * 100
    republican_percentage = (republican_votes / total_votes) * 100
    third_party_percentage = (third_party_votes / total_votes) * 100
    return democratic_percentage, republican_percentage, third_party_percentage

file_path = 'election-night-results-report.csv'
democratic_percentage, republican_percentage, third_party_percentage = calculate_democratic_percentage(file_path)
print(f"Total votes: {total_votes}")
print(f"Democratic votes: {democratic_votes}")
print(f"Democratic votes percentage: {democratic_percentage}%")

print(f"Republican votes: {republican_votes}")
print(f"Republican votes percentage: {republican_percentage}%")

print(f"Third party votes: {third_party_votes}")
print(f"Third party votes percentage: {third_party_percentage}%")