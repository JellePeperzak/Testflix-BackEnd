import pandas as pd

from dataPreparation import prepareData
# prepareData accepts two arguments: (raw_data_path, prepared_data_path) and returns True
from linearRegression import linearRegression, generateResidualSubplots
# linearRegression requires three arguments: (prepared_data_path, independent variable, dependent variable)
# and returns X, y_pred, residuals, model, and robust_model
from testAssumptions import generateLinearityPlot, testNormality, testHomoscedasticity, testIndependence, generateLinearitySubPlots, generateIndependenceSubplots
# generateLinearityPlot accepts three arguments: (prepared_data_path, independent_variable, dependent_variable) and returns True
# testNormality accepts one argument: (residuals) and returns the statistic, p-value and True/False depending on whether the assumption was violated.t
# testHomoscedasticity accepts four arguments: (residuals, y_pred, normality, X) and returns the statistic, p-value and True/False depending on whether the assumption was violated.

raw_data_path = 'analysis/datasets/rawData.csv'
prepared_data_path = 'analysis/datasets/preparedData.csv'

independent_variable = 'eval'
dependent_variable = 'se'
dependent_variables = ['grat_all', 'grat_all_no_se', 'cn', 'en', 'se']
df_assumptions = pd.DataFrame(columns=['Dependent Variable', 'Normality', 'Homoscedasticity'])
# Options for dependent variables: [cn, en, se, grat_all]

# PREPARE DATA (only run once if the raw data changes)
success_preparation = prepareData(raw_data_path, prepared_data_path)
if (success_preparation):
    print("Data was successfully prepared!")

all_models = []
dataframe_index = -1
# GENERATE LINEARITY PLOT BASED ON DATA
for dependent_variable in dependent_variables:
    dataframe_index += 1

    # Generate plots for LINEARITY and INDEPENDENCE assumptions
    success_linearity = generateLinearityPlot(prepared_data_path, independent_variable, dependent_variable)

    # PERFORM LINEAR REGRESSION AND RETURN STATISTICS DATA REQUIRED FOR OTHER ASSUMPTION TESTS
    X, y_pred, residuals, model, robust_model = linearRegression(prepared_data_path, independent_variable, dependent_variable)

    # TEST ASSUMPTION OF NORMALITY OF RESIDUALS
    statistic_normality, p_value_normality, normality = testNormality(residuals)

    # TEST ASSUMPTION OF HOMOSCEDASCTICITY 
    statistic_homo, p_value_homo, homoscedasticity = testHomoscedasticity(residuals, y_pred, normality, X)

    # Select which model to use based on the outcome of assumption testing
    test_model = model if normality else robust_model

    dw_statistic, bg_test_stat, bg_p_value = testIndependence(raw_data_path, prepared_data_path, dependent_variable, independent_variable, test_model)

    all_models.append(test_model)
    df_assumptions.loc[dataframe_index] = [dependent_variable, p_value_normality, p_value_homo]

    print('\n\t--- ASSUMPTIONS ---')
    print(f"Independent variable: {independent_variable}")
    print(f"Dependent variable: {dependent_variable}")
    print(f"Normality: {"\033[31mViolated\033[39m" if not normality else "\033[32mSatisfied\033[39m"}, p={p_value_normality}, stat={statistic_normality}")
    print(f"Homoscedasticity: {"\033[31mViolated\033[39m" if not homoscedasticity else "\033[32mSatisfied\033[39m"}, p={p_value_homo}, stat={statistic_homo}")
    print("Linearity: \033[33mCheck plot in 'plots' folder\033[0m")
    print(f"Independence: \033[33mDurbin-Watson statistic: {dw_statistic}\033[0m")
    print(f"Independence: \033[33mBreusch-Godfrey statistic: {bg_test_stat}, pvalue: {bg_p_value}\033[0m")
    print("\n")
    print(test_model.summary())

generateLinearitySubPlots(prepared_data_path, independent_variable, dependent_variables)
generateIndependenceSubplots(raw_data_path, prepared_data_path, dependent_variables, independent_variable)
generateResidualSubplots(prepared_data_path, dependent_variables, independent_variable, all_models)

print(df_assumptions)
