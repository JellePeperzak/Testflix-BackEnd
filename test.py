import pandas as pd

data_path = "data_3feb.csv"

df = pd.read_csv(data_path, header=0)

df_unique = df['condition_id'].unique()

numbers = []
for i in range(36):
    numbers.append(i)

print(numbers)

print(len(df_unique))

missing_conditions = [c for c in numbers if c not in df_unique]

print(missing_conditions)
