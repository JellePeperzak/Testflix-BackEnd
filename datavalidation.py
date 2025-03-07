import pandas as pd

data_path = "data_9feb.csv"

df = pd.read_csv(data_path, header=0)

df['time_total'] = abs(df['time_finish'] - df['time_start']) / (1000)
df['time_task1'] = abs(df['task1_finish'] - df['task1_start']) / (1000)
df['time_task2'] = abs(df['task2_finish'] - df['task2_start']) / (1000)
df['time_task3'] = abs(df['task3_finish'] - df['task3_start']) / (1000)

print(f'\n\t\033[34m--- ALL TIMES PER PARTICIPANT ---\033[0m')
print(df[['time_total', 'time_task1', 'time_task2', 'time_task3']])

df_total_sorted = df['time_total'].sort_values(ascending=False)
df_task1_sorted = df['time_task1'].sort_values(ascending=False)
df_task2_sorted = df['time_task2'].sort_values(ascending=False)
df_task3_sorted = df['time_task3'].sort_values(ascending=False)

df_list = [df_total_sorted, df_task1_sorted, df_task2_sorted, df_task3_sorted]
df_names = ['TIME TOTAL', 'TASK 1', 'TASK2', 'TASK3']
name_index = -1
print('\n\n\t--- TOP 5 HIGHEST TIMES PER TASK ---')
for frame in df_list:
    name_index += 1
    print(f'\033[34m--- {df_names[name_index]} ---\033[0m')
    print(frame.head(5))
    print('\n')
#df.to_csv(data_path, index=False)

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
