import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def createPlot(ax, data_path, title, palette):
    df = pd.read_csv(data_path, header=0)

    df['score (jittered)'] = df['score'] + np.random.uniform(-0.1, 0.1, size=len(df))  # Vertical jitter

    # Create the swarm plot
    sns.swarmplot(
        x='algorithm',  # Categorical variable on X-axis
        y='score (jittered)',       # Continuous variable on Y-axis
        hue='task',  # Second categorical variable (color-coded)
        data=df,
        dodge=True,        # Separates hue categories for clarity
        size=4,
        palette=palette,
        ax=ax
    )

    # Customize the plot
    ax.set_title(title)
    ax.legend_.remove()  # Remove individual legends from subplots

path_names = ['cn1', 'cn2', 'en1', 'se1', 'eval_1', 'eval_2', 'eval_3']

# Create subplots (2 rows, 4 columns)
fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(16, 10))  # Adjust the figure size accordingly

# Flatten axes array to make indexing easier
axes = axes.flatten()

# Define a color palette (this palette will be used across all plots)
palette = sns.color_palette("muted")

for i, name in enumerate(path_names):
    path = f"analysis/datasets/rawDataPlots/{name}.csv"
    createPlot(axes[i], path, title=f"Raw data distribution for {name}", palette=palette)

# Hide the last (empty) subplot to make space for the legend
axes[-1].axis('off')  # Hide the last axes (empty space)

# Create a custom legend with only the unique task mappings
# Get the unique hue values from the first dataset
hue_values = ['task1', 'task2', 'task3']  # Replace with actual unique task names if needed

# Create the handles for the legend (one for each unique hue value)
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=palette[i], markersize=10) for i in range(len(hue_values))]

# Add the shared legend in the position of the last subplot
fig.legend(handles=handles, labels=hue_values, title="task", loc='center', bbox_to_anchor=(0.80, 0.425), borderaxespad=0.)


# Adjust layout to avoid overlapping
plt.tight_layout()

# Show the plots
plt.savefig(f"analysis/plots/rawdata.png")
