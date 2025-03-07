import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ks_1samp, norm
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan, het_white, acorr_breusch_godfrey
from statsmodels.stats.stattools import durbin_watson

def generateLinearityPlot(prepared_data_path, independent_variable, dependent_variable):
    df = pd.read_csv(prepared_data_path, header=0)

    # Calculate the line of best fit (linear regression)
    # Fit a linear model: y = mx + b
    x = df[independent_variable]
    y = df[dependent_variable]

    slope, intercept = np.polyfit(x, y, 1)

    # Create the line based on the slope and intercept
    y_fit = slope * x + intercept

    # Add jitter to give a better impression of density in the plot
    jitter_amount = 0.2
    x_jittered = x + np.random.normal(0, jitter_amount, len(x))
    y_jittered = y + np.random.normal(0, jitter_amount, len(y))

    # Plot the line of best fit
    plt.figure(figsize=(8, 6))
    plt.scatter(x_jittered, y_jittered, color='blue')
    plt.plot(x, y_fit, label="Best fit line", color='red', linestyle='--')
    plt.title(f"Scatter Plot: {independent_variable} vs {dependent_variable}")
    plt.xlabel(f"X ({independent_variable})")
    plt.ylabel(f"Y ({dependent_variable})")
    plt.savefig(f"analysis/plots/{dependent_variable}_linearity.png")
    plt.close()

    return True

def generateLinearitySubPlots(prepared_data_path, independent_variable, dependent_variables):
    df = pd.read_csv(prepared_data_path, header=0)

    # Calculate the line of best fit (linear regression)
    # Fit a linear model: y = mx + b
    x = df[independent_variable]
    y_values = [df[dep_var] for dep_var in dependent_variables]

    # Compute slopes and intercepts for best-fit lines
    fits = [np.polyfit(x, y, 1) for y in y_values]
    y_fits = [slope * x + intercept for slope, intercept in fits]

    # Add jitter to x and y values for better density visualization
    jitter_amount = 0.2
    x_jittered = x + np.random.normal(0, jitter_amount, len(x))
    y_jittered = [y + np.random.normal(0, jitter_amount, len(y)) for y in y_values]


    fig, axes = plt.subplots(3, 2, figsize=(12, 10))
    
    # Titles for subplots
    subplot_titles = [
        f"{independent_variable} vs {dependent_variables[0]}",
        f"{independent_variable} vs {dependent_variables[1]}",
        f"{independent_variable} vs {dependent_variables[2]}",
        f"{independent_variable} vs {dependent_variables[3]}",
        f"{independent_variable} vs {dependent_variables[4]}"
    ]

    # Loop through subplots and plot data
    for i, ax in enumerate(axes.flat):  # Flatten the 2D array to iterate easily
        if i < 5:
            ax.scatter(x_jittered, y_jittered[i], color='blue', alpha=0.6, label="Data (jittered)")
            ax.plot(x, y_fits[i], color='red', linestyle='--', label="Best fit line")
            ax.set_title(subplot_titles[i])
            ax.set_xlabel(f"X ({independent_variable})")
            ax.set_ylabel(f"Y ({dependent_variables[i]})")
            ax.legend()

    axes = axes.flatten()
    axes[-1].axis('off')  # Hide the last axes (empty space)

    # Adjust layout to avoid overlapping
    plt.tight_layout()

    # Save and close figure
    plt.savefig(f"analysis/plots/SUBPLOTS_linearity.png")
    plt.close()

    return True

def testNormality(residuals):
    # Standardize the residuals (optional, if you want to compare to N(0, 1))
    standardized_residuals = (residuals - np.mean(residuals)) / np.std(residuals)

    # Perform the K-S test comparing residuals to a standard normal distribution
    ks_test = ks_1samp(standardized_residuals, cdf=norm.cdf)
    statistic = ks_test.statistic
    p_value = ks_test.pvalue

    '''# Output results
    print("--- NORMALITY ---")
    print(f"Kolmogorov-Smirnov Statistic: {statistic}")
    print(f"Kolmogorov-Smirnov P-value: {p_value}")
    print(f"Assumption: {"\033[31mViolated\033[39m" if p_value < 0.05 else "\033[32mSatisfied\033[39m"}")'''

    return statistic, p_value, p_value > 0.05


def testHomoscedasticity(residuals, y_pred, normality, X):
    # Perform heteroscedasticity test and extract results
    # Check normality assumption to decide which test to run
    if normality == True:
        # p-value should be greater than 0.05 in order not to violate the assumption
        bp_test = het_breuschpagan(residuals, X)
        statistic, p_value = bp_test[0], bp_test[1]

        '''    # Print results
        print("--- HOMOSCEDASTICITY ---")
        print(f"Breusch-Pagan Statistic: {statistic}")
        print(f"Breusch-Pagan P-value: {p_value}")
        print(f"Assumption: {"\033[31mViolated\033[39m" if p_value < 0.05 else "\033[32mSatisfied\033[39m"}")'''
    else:
        # p-value should be greater than 0.05 in order not to violate the assumption
        white_test = het_white(residuals, sm.add_constant(np.column_stack((y_pred, y_pred**2))))
        statistic, p_value = white_test[0], white_test[1]

        '''        # Print results
        print("--- HOMOSCEDASTICITY ---")
        print(f"White's Statistic: {statistic}")
        print(f"White's P-value: {p_value}")
        print(f"Assumption: {"\033[31mViolated\033[39m" if p_value < 0.05 else "\033[32mSatisfied\033[39m"}")'''

    return statistic, p_value, p_value > 0.05

def testIndependence(raw_data_path, prepared_data_path, dependent_variable, independent_variable, test_model):
    df_prepared = pd.read_csv(prepared_data_path, header=0)
    df_raw = pd.read_csv(raw_data_path, header=0)

    # Sort the prepared data by Participant and then by Algorithm in a specified order
    def get_algorithm_order(x):
        algorithm_order = []
        row_data = df_raw[df_raw['id'] == x]
        columns = ['first_algorithm', 'second_algorithm', 'third_algorithm']
        for column in columns:
            algorithm = row_data[column].iloc[0]
            algorithm_order.append(algorithm)
        return algorithm_order
    
    df_prepared['algorithm_sort_order'] = df_prepared.apply(lambda row: get_algorithm_order(row['id']).index(row['algorithm']), axis=1)

    # Sort by 'id' and then by the custom 'algorithm_sort_order'
    df_sorted = df_prepared.sort_values(by=['id', 'algorithm_sort_order'])

    # Drop the temporary sorting order column
    #df_sorted = df_sorted.drop(columns=['algorithm_sort_order'])

    # Train a new model based on the sorted data
    x = df_sorted[independent_variable]
    y = df_sorted[dependent_variable]

    # Add a constant for the intercept in the regression model
    X = sm.add_constant(x)

    # Fit a linear regression model and run durbin_watson test
    model_algorithm = sm.OLS(y, X).fit()

    dw_statistic = durbin_watson(test_model.resid)
    bg_results = acorr_breusch_godfrey(test_model, nlags=1)  # You can change nlags based on your needs
    bg_test_stat, bg_p_value, f_stat, f_p_value = bg_results

    # Compute residuals
    df_sorted["residuals"] = model_algorithm.resid

    # Group residuals by timestamps (algorithm_sort_order)
    timestamps = df_sorted["algorithm_sort_order"].unique()
    residuals_grouped = [df_sorted[df_sorted["algorithm_sort_order"] == t]["residuals"].values for t in timestamps]

    algorithms = [1, 2, 3]
    algorithms_grouped = [df_sorted[df_sorted["algorithm"] == t]["residuals"].values for t in algorithms]

    # Create the violin plot
    plt.figure(figsize=(8, 5))
    plt.violinplot(residuals_grouped, showmeans=True, showmedians=True)

    # Customize the plot
    plt.axhline(y=0, color='r', linestyle='--')  # Add a horizontal line at 0
    plt.xticks(range(1, len(timestamps) + 1), timestamps)  # Match x-axis to timestamps
    plt.xlabel('Timestamps')
    plt.ylabel('Residuals')
    plt.title('Residuals vs. Timestamps')
    plt.savefig(f"analysis/plots/{dependent_variable}_independence.png")
    plt.close()

    # Create the violin plot
    plt.figure(figsize=(8, 5))
    plt.violinplot(algorithms_grouped, showmeans=True, showmedians=True)

    # Customize the plot
    plt.axhline(y=0, color='r', linestyle='--')  # Add a horizontal line at 0
    plt.xticks(range(1, len(algorithms) + 1), algorithms)  # Match x-axis to timestamps
    plt.xlabel('Algorithms')
    plt.ylabel('Residuals')
    plt.title('Residuals vs. Algorithms')
    plt.savefig(f"analysis/plots/{dependent_variable}_independence_algorithms.png")
    plt.close()

    return dw_statistic, bg_test_stat, bg_p_value

def generateIndependenceSubplots(raw_data_path, prepared_data_path, dependent_variables, independent_variable):
    df_prepared = pd.read_csv(prepared_data_path, header=0)
    df_raw = pd.read_csv(raw_data_path, header=0)

    # Sort the prepared data by Participant and then by Algorithm in a specified order
    def get_algorithm_order(x):
        algorithm_order = []
        row_data = df_raw[df_raw['id'] == x]
        columns = ['first_algorithm', 'second_algorithm', 'third_algorithm']
        for column in columns:
            algorithm = row_data[column].iloc[0]
            algorithm_order.append(algorithm)
        return algorithm_order
    
    df_prepared['algorithm_sort_order'] = df_prepared.apply(lambda row: get_algorithm_order(row['id']).index(row['algorithm']), axis=1)

    # Sort by 'id' and then by the custom 'algorithm_sort_order'
    df_sorted = df_prepared.sort_values(by=['id', 'algorithm_sort_order'])

    # Drop the temporary sorting order column
    #df_sorted = df_sorted.drop(columns=['algorithm_sort_order'])

    # Train a new model based on the sorted data
    x = df_sorted[independent_variable]
    y_values = [df_sorted[dep_var] for dep_var in dependent_variables]

    # Add a constant for the intercept in the regression model
    X = sm.add_constant(x)

    # Fit a linear regression model and run durbin_watson test
    model_algorithms = [sm.OLS(y_value, X).fit() for y_value in y_values]
    
    #dw_algorithm = durbin_watson(model_algorithm.resid)            Durbin-Watson might not be relevant due to there only being 3 timestamps

    # Compute residuals
    variable_index = -1
    for model_algorithm in model_algorithms:
        variable_index += 1
        df_sorted[f"residuals_{dependent_variables[variable_index]}"] = model_algorithm.resid

    # Group residuals by timestamps (algorithm_sort_order)
    timestamps = df_sorted["algorithm_sort_order"].unique()
    all_residuals_grouped_timestamps = []
    for dep_var in dependent_variables:
        residuals_grouped_timestamps = [df_sorted[df_sorted["algorithm_sort_order"] == t][f"residuals_{dep_var}"].values for t in timestamps]
        all_residuals_grouped_timestamps.append(residuals_grouped_timestamps)

    algorithms = [1, 2, 3]
    all_residuals_grouped_algorithms = []
    for dep_var in dependent_variables:
        residuals_grouped_algorithms = [df_sorted[df_sorted["algorithm"] == t][f"residuals_{dep_var}"].values for t in algorithms]
        all_residuals_grouped_algorithms.append(residuals_grouped_algorithms)

    # Create violin subplots (timestamps)
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    subplot_titles_timestamps = [
        f"Residuals vs Timestamps ({dep_var})" for dep_var in dependent_variables
    ]

    # Plot residuals
    for i, ax in enumerate(axes.flat[:len(subplot_titles_timestamps)]):
        ax.violinplot(all_residuals_grouped_timestamps[i], showmeans=True, showmedians=True)
        ax.axhline(y=0, color='r', linestyle='--')
        ax.set_xticks(range(1, len(timestamps) + 1))
        ax.set_xticklabels(timestamps)
        ax.set_xlabel('Timestamps')
        ax.set_ylabel('Residuals')
        ax.set_title(subplot_titles_timestamps[i])
    
    plt.tight_layout()
    plt.savefig("analysis/plots/SUBPLOTS_independence_timestamps.png")
    plt.close()

    # Create violin subplots (Algorithms)
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    subplot_titles_algorithms = [
        f"Residuals vs Algorithms ({dep_var})" for dep_var in dependent_variables
    ]

    # Plot residuals
    for i, ax in enumerate(axes.flat[:len(subplot_titles_algorithms)]):
        ax.violinplot(all_residuals_grouped_algorithms[i], showmeans=True, showmedians=True)
        ax.axhline(y=0, color='r', linestyle='--')
        ax.set_xticks(range(1, len(algorithms) + 1))
        ax.set_xticklabels(algorithms)
        ax.set_xlabel('Algorithms')
        ax.set_ylabel('Residuals')
        ax.set_title(subplot_titles_algorithms[i])
    
    plt.tight_layout()
    plt.savefig("analysis/plots/SUBPLOTS_independence_algorithms.png")
    plt.close()
    
'''
--- CODE TO GENERATE TASK ORDER AND TRAIN MODEL FOR DURBIN_WATSON ---
    --- This code is irrelevant, considering this generates the same order as the implemented algorithm order does ---
# Generate task numbers in preparation for running the same test on task order
    def get_task_number(id_number, algorithm_number, number_list, order_list):
        df_participant = df_raw[df_raw['id'] == id_number]
        first_algorithm = df_participant['first_algorithm'].iloc[0]
        second_algorithm = df_participant['second_algorithm'].iloc[0]
        if first_algorithm == algorithm_number:
            task_number = df_participant['first_task'].iloc[0]
            order_list.append(1)
        elif second_algorithm == algorithm_number:
            task_number = df_participant['second_task'].iloc[0]
            order_list.append(2)
        else:
            task_number = df_participant['third_task'].iloc[0]
            order_list.append(3)

        number_list.append(task_number)
        return number_list, order_list
    
    # Use task number generator to generate the tasks and sorting order, and add relevant columns to df_sorted
    task_numbers = []
    task_order = []
    for row in df_sorted.itertuples():
        task_numbers, task_order = get_task_number(row.id, row.algorithm, task_numbers, task_order)

    df_sorted['task'] = task_numbers
    df_sorted['task_sort_order'] = task_order

    # Sort by 'id' and then by the custom 'task_sort_order'
    df_sorted = df_sorted.sort_values(by=['id', 'task_sort_order'])

    # Drop the temporary sorting order column
    df_sorted = df_sorted.drop(columns=['task_sort_order'])

    # Train a new model based on the sorted data
    x = df_sorted[independent_variable]
    y = df_sorted[dependent_variable]

    # Add a constant for the intercept in the regression model
    X = sm.add_constant(x)

    # Fit a linear regression model and run durbin_watson test
    model_task = sm.OLS(y, X).fit()
    dw_task = durbin_watson(model_task.resid)
'''