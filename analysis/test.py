import pandas as pd

#"age","gender","nationality","experience","consumption"

raw_data_path = 'analysis/datasets/rawData.csv'

df = pd.read_csv(raw_data_path, header=0)

#print(df['gender'].value_counts())
#print(df['age'].mean())
#print(df['age'].std())
#print(df['nationality'].value_counts())
print(df['experience'].value_counts())