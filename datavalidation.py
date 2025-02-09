import pandas as pd

data_path = "data_9feb.csv"

df = pd.read_csv(data_path, header=0)

df_unique = df['condition_id'].unique()

numbers = []
for i in range(36):
    numbers.append(i)

print(numbers)

print(len(df_unique))

missing_conditions = [c for c in numbers if c not in df_unique]

print(missing_conditions)

'''
--- GENERATE TIME DIFFERENCE DATA (IN SECONDS) BASED ON TIME START AND TIME FINISH ---
df['time_total'] = abs(df['time_finish'] - df['time_start']) / (1000)
df['time_task1'] = abs(df['task1_finish'] - df['task1_start']) / (1000)
df['time_task2'] = abs(df['task2_finish'] - df['task2_start']) / (1000)
df['time_task3'] = abs(df['task3_finish'] - df['task3_start']) / (1000)

print(df[['time_total', 'time_task1', 'time_task2', 'time_task3']])

df.to_csv(data_path, index=False)
'''

'''
--- GENERATE MISSING CONDITIONS ---
df_unique = df['condition_id'].unique()

numbers = []
for i in range(36):
    numbers.append(i)

print(numbers)

print(len(df_unique))

missing_conditions = [c for c in numbers if c not in df_unique]

print(missing_conditions)
'''
