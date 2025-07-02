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
            if not row['Precinct'].startswith('SEA ') or row['Race'] != 'State of Washington US President & Vice President':
                continue
            if row['Party'] == 'Democratic Party Nominees':
                democratic_votes += int(row['SumOfCount'])
            if row['Party'] == 'Republican Party Nominees':
                republican_votes += int(row['SumOfCount'])
            if row['Party'] != 'Democratic Party Nominees' and row['Party'] != 'Republican Party Nominees' and row['Party'] != 'NP':
                third_party_votes += int(row['SumOfCount'])
    
    total_votes = democratic_votes + republican_votes + third_party_votes
    democratic_percentage = (democratic_votes / total_votes) * 100
    republican_percentage = (republican_votes / total_votes) * 100
    third_party_percentage = (third_party_votes / total_votes) * 100
    return democratic_percentage, republican_percentage, third_party_percentage

file_path = 'November_2020_General_Final_Precinct_Results.csv'
democratic_percentage, republican_percentage, third_party_percentage = calculate_democratic_percentage(file_path)
print(f"Total votes: {total_votes}")
print(f"Democratic votes: {democratic_votes}")
print(f"Democratic votes percentage: {democratic_percentage}%")

print(f"Republican votes: {republican_votes}")
print(f"Republican votes percentage: {republican_percentage}%")

print(f"Third party votes: {third_party_votes}")
print(f"Third party votes percentage: {third_party_percentage}%")
