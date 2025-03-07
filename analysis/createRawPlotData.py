# CODE USED TO GENERATE THE DATA IN THE rawDataPlots FOLDER
import pandas as pd

raw_data_path = 'analysis/datasets/rawData.csv'

df_raw = pd.read_csv(raw_data_path, header=0)

variables = {
    'cn': 2,
    'en': 1,
    'se': 1,
    'eval': 3
}

def createDataFrame(var_name, var_type, data_path):
    df = pd.DataFrame()
    df['id'] = df_raw['id']
    df[f"{var_name}_1"] = df_raw[f"{var_name}_1"]
    df[f"{var_name}_2"] = df_raw[f"{var_name}_2"]
    df[f"{var_name}_3"] = df_raw[f"{var_name}_3"]
    df['first_task'] = df_raw['first_task']
    df['second_task'] = df_raw['second_task']
    df['third_task'] = df_raw['third_task']
    df['first_algorithm'] = df_raw['first_algorithm']
    df['second_algorithm'] = df_raw['second_algorithm']
    df['third_algorithm'] = df_raw['third_algorithm']

    df_new = df.melt(id_vars=['id', 'first_task', 'second_task', 'third_task', 'first_algorithm', 'second_algorithm', 'third_algorithm'], value_vars=[f"{var_name}_1", f"{var_name}_2", f"{var_name}_3"], var_name=f"{var_type}_type", value_name='score')

    df_new['algorithm'] = df_new[f"{var_type}_type"].str.extract(r'(\d)$')

    print(df_new)

    task_order = []
    for row in df_new.itertuples():
        print(f"First Task: {row.first_task}, {type(row.first_task)}")
        print(f"Algorithm: {row.algorithm}, {type(row.algorithm)}")
        algorithm = int(row.algorithm)
        if row.first_algorithm == algorithm:
            print("ding!")
            task_order.append(row.first_task)
        elif row.second_algorithm == algorithm:
            print("dingding!")
            task_order.append(row.second_task)
        elif row.third_algorithm == algorithm:
            print("dingdingding!")
            task_order.append(row.third_task)
        else:
            print(f"No task found for row {row.Index}")

    df_new['task'] = task_order
    df_new = df_new.drop(columns=['id', 'first_task', 'second_task', 'third_task', 'first_algorithm', 'second_algorithm', 'third_algorithm', f"{var_type}_type"])

    df_new.to_csv(data_path, index=False)
    print(f"Dataframe for {var_name} is successfully saved in the plot data folder")

createDataFrame('cn_1', 'cn', 'analysis/datasets/rawDataPlots/cn1.csv')
createDataFrame('cn_2', 'cn', 'analysis/datasets/rawDataPlots/cn2.csv')

createDataFrame('en_1', 'en', 'analysis/datasets/rawDataPlots/en1.csv')

createDataFrame('se_1', 'se', 'analysis/datasets/rawDataPlots/se1.csv')

createDataFrame('eval_1', 'cn', 'analysis/datasets/rawDataPlots/eval_1.csv')
createDataFrame('eval_2', 'cn', 'analysis/datasets/rawDataPlots/eval_2.csv')
createDataFrame('eval_3', 'cn', 'analysis/datasets/rawDataPlots/eval_3.csv')








