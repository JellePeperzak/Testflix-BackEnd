import pandas as pd

# In order to create the bootstrap, we need to perform the data preparation steps so that each participant is
# watered down to the following list of values:
# [cn, en, se, grat_all, eval]
# Note that each participant will translate to three observations, resulting in a dataset of 6 rows to bootstrap.

# STEP 1: Import the dataset with participant responses
def prepareData(raw_data_path, prepared_data_path):
    df = pd.read_csv(raw_data_path, header=0)

    # STEP 2: Perform the data preparation steps as described in the Data Analysis Notes file
    # 1. Compute the average satisfaction score for every gratification category.
    def addAverageColumns(df, category_name, statement_count):
        for algorithm_number in range(1, 4):
            column_names = []
            for statement_number in range(1, statement_count+1):
                col_name = f"{category_name}_{statement_number}_{algorithm_number}"
                column_names.append(col_name)
            new_col_name = f"{category_name}_avg_{algorithm_number}"
            df[new_col_name] = df[column_names].mean(axis=1)
        return df


    #   Convenient Navigability
    df = addAverageColumns(df, 'cn', 2)

    #   Entertainment
    df = addAverageColumns(df, 'en', 1)

    #   Social Enhancement
    df = addAverageColumns(df, 'se', 1)

    #   Recommender Evaluation
    df = addAverageColumns(df, 'eval', 3)

    #   Divide participant's data over three rows, one for every task
    #relevant_columns = ['cn_avg_1', 'cn_avg_2', 'cn_avg_3', 'en_avg_1', 'en_avg_2', 'en_avg_3', 'se_avg_1', 'se_avg_2', 'se_avg_3', 'eval_avg_1', 'eval_avg_2', 'eval_avg_3',]
    df_cn = df.melt(id_vars=['id', 'first_task', 'second_task', 'third_task', 'first_algorithm', 'second_algorithm', 'third_algorithm'], value_vars=['cn_avg_1', 'cn_avg_2', 'cn_avg_3'], var_name='cn_type', value_name='cn')
    df_en = df.melt(id_vars=['id', 'first_task', 'second_task', 'third_task', 'first_algorithm', 'second_algorithm', 'third_algorithm'], value_vars=['en_avg_1', 'en_avg_2', 'en_avg_3'], var_name='en_type', value_name='en')
    df_se = df.melt(id_vars=['id', 'first_task', 'second_task', 'third_task', 'first_algorithm', 'second_algorithm', 'third_algorithm'], value_vars=['se_avg_1', 'se_avg_2', 'se_avg_3'], var_name='se_type', value_name='se')
    df_eval = df.melt(id_vars=['id', 'first_task', 'second_task', 'third_task', 'first_algorithm', 'second_algorithm', 'third_algorithm'], value_vars=['eval_avg_1', 'eval_avg_2', 'eval_avg_3'], var_name='eval_type', value_name='eval')

    df_new = df_cn.copy()

    df_new['algorithm'] = df_new['cn_type'].str.replace(r'\D', '', regex=True)

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
    print(df_new)
    df_new.drop(columns=['cn_type'], inplace=True)
    df_new['en'] = df_en['en']
    df_new['se'] = df_se['se']
    df_new['eval'] = df_eval['eval']
    df_new['grat_all_no_se'] = (df_new['en'] + df_new['cn']) / 2

    # Compute average gratification score for every row
    grat_columns = ['cn', 'en', 'se']
    df_new['grat_all'] = df_new[grat_columns].mean(axis=1)

    # STEP 3: Save the prepared data in a .csv file
    df_new.to_csv(prepared_data_path, index=False)

    return True