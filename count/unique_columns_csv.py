import pandas as pd

df = pd.read_csv('c:/Users/Chen/Downloads/election-night-results-report.csv')

filtered_df = df[df['Race'] == 'President and Vice President of the United States President and Vice President of the United States']
counter_types = filtered_df['CounterType'].unique()


print('\033[1;41m' + 'CounterType in Presidential Race' + '\033[0m')
for counter_type in counter_types:
    print(counter_type)

race_types = df['Race'].unique()

print('\n' + '\033[1;41m' + 'Race' + '\033[0m')
for race_type in race_types:
    print(race_type)

