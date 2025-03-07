import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

def linearRegression(data_path, variable_independent, variable_dependent):
    # Import and define sample data
    df = pd.read_csv(data_path, header=0)
    x = df[variable_independent]
    y = df[variable_dependent]

    # Add a constant for the intercept in the regressino model
    X = sm.add_constant(x)

    # Fit a linear regression model and generate a robust alternative
    model = sm.OLS(y, X).fit()
    robust_model = model.get_robustcov_results()
    y_pred = model.predict(X)

    # Calculate residuals
    residuals = y - y_pred

    # Plot residuals against predicted values
    plt.scatter(y_pred, residuals, color="blue", label="Residuals")
    plt.axhline(y=0, color="red", linestyle="--", label="Zero Residual Line")  # Reference line at y=0

    # Add labels and title
    plt.title("Residuals vs Predicted Values")
    plt.xlabel("Predicted Values")
    plt.ylabel("Residuals")
    plt.legend()

    # Show plot
    plt.savefig(f"analysis/plots/{variable_dependent}_residuals.png")
    plt.close()

    return X, y_pred, residuals, model, robust_model


def generateResidualSubplots(prepared_data_path, dependent_variables, independent_variable, models):
    df = pd.read_csv(prepared_data_path, header=0)
    x = df[independent_variable]
    y_values = [df[dep_var] for dep_var in dependent_variables]

    X = sm.add_constant(x)
    y_preds = []
    for model in models:
        y_preds.append(model.predict(X))
    
    residuals = []
    for i, y_pred in enumerate(y_preds):
        residuals.append(y_values[i] - y_pred)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    subplot_titles = [
        f"Residuals vs Predicted Values ({dep_var})" for dep_var in dependent_variables
    ]

    for i, ax in enumerate(axes.flat[:len(dependent_variables)]):  # Flatten the 2D array to iterate easily
        ax.scatter(y_preds[i], residuals[i], color="blue", label="Residuals")
        ax.axhline(y=0, color="red", linestyle="--", label="Zero Residual Line")
        ax.set_title(subplot_titles[i])
        ax.set_xlabel(f"Predicted Values")
        ax.set_ylabel(f"Residuals")
        ax.legend()
    
    # Adjust layout to avoid overlapping
    plt.tight_layout()

    # Save and close figure
    plt.savefig(f"analysis/plots/SUBPLOTS_residuals.png")
    plt.close()