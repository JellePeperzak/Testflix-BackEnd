import pandas as pd

raw_data_path = 'analysis/datasets/rawData.csv'

df = pd.read_csv(raw_data_path, header=0)

value_count1 = df['first_task'].value_counts()
value_count2 = df['second_task'].value_counts()
value_count3 = df['third_task'].value_counts()

print(value_count1)
print(value_count2)
print(value_count3)


'''
--- GENERATE CRONBACHS ALPHA VALUES ---

import pandas as pd
import pingouin as pg

#"age","gender","nationality","experience","consumption"

raw_data_path = 'analysis/datasets/rawData.csv'

df = pd.read_csv(raw_data_path, header=0)

# eval_1_3 refers to FIRST STATEMENT and THIRD ALGORITHM

eval_cols_1 = ["eval_1_1","eval_1_2","eval_1_3"]
eval_cols_2 = ["eval_2_1","eval_2_2","eval_2_3"]
eval_cols_3 = ["eval_3_1","eval_3_2","eval_3_3"]
df_eval1 = df[eval_cols_1]
df_eval2 = df[eval_cols_2]
df_eval3 = df[eval_cols_3]

eval_melt_1 = df_eval1.melt(value_name='eval1')['eval1']
eval_melt_2 = df_eval2.melt(value_name='eval2')['eval2']
eval_melt_3 = df_eval3.melt(value_name='eval3')['eval3']

df_cron_eval = pd.concat([eval_melt_1, eval_melt_2, eval_melt_3], axis=1)

alpha_eval, _ = pg.cronbach_alpha(df_cron_eval)

print(f"Cronbach's Alpha (eval): {alpha_eval:.3f}")

print(df_cron_eval)

cn_cols_1 = ["cn_1_1","cn_1_2","cn_1_3"]
cn_cols_2 = ["cn_2_1","cn_2_2","cn_2_3"]
df_cn1 = df[cn_cols_1]
df_cn2 = df[cn_cols_2]

cn_melt_1 = df_cn1.melt(value_name='cn1')['cn1']
cn_melt_2 = df_cn2.melt(value_name='cn2')['cn2']

df_cron_cn = pd.concat([cn_melt_1, cn_melt_2], axis=1)

alpha_cn, _ = pg.cronbach_alpha(df_cron_cn)

print(f"Cronbach's Alpha (cn): {alpha_cn:.3f}")
'''




# --- LINES OF CODE TO GENERATE DESCRIPTIVES --
#print(df['gender'].value_counts())
#print(df['age'].mean())
#print(df['age'].std())
#print(df['age'].max())
#print(df['age'].min())
#print(df['nationality'].value_counts())
#print(df['experience'].mean())
#print(df['experience'].std())