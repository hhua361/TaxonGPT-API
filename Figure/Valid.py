import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data from the provided CSV file
file_path = "E:/Evaluate_results_for_all_datasets/Evaluate_table/Quantity/quantity_valid.csv"
data = pd.read_csv(file_path)

# Remove the first row (which contains column names for methods)
data_cleaned = data.drop(0)

# Function to convert percentage strings to floats
def convert_to_float(value):
    if isinstance(value, str) and '%' in value:
        return float(value.replace('%', '')) / 100
    return float(value)

# Apply the conversion to the relevant columns
for col in data_cleaned.columns[1:]:
    data_cleaned[col] = data_cleaned[col].apply(convert_to_float)

# Extract datasets, api_data and web_data
datasets = data_cleaned['Valid-state'].values
api_data = data_cleaned.iloc[:, 1:6].values
web_data = data_cleaned.iloc[:, 6:11].values

# Improved bar chart with enhanced aesthetics inspired by the provided example
fig, ax1 = plt.subplots(figsize=(16, 7))

# Plotting for each dataset
width = 0.6  # Width of the bars
x_labels = []

methods = ['API', 'Web']  # Define methods for positioning
x = np.arange(len(datasets) * 2, step=2)  # Increased space between groups

api_means_list = []
web_means_list = []

for i, dataset in enumerate(datasets):
    api_means = api_data[i].mean()
    api_errors = api_data[i].std() / np.sqrt(len(api_data[i]))
    web_means = web_data[i].mean()
    web_errors = web_data[i].std() / np.sqrt(len(web_data[i]))

    api_means_list.append(api_means)
    web_means_list.append(web_means)

    ax1.bar(x[i] - width/2, api_means, width, yerr=api_errors, capsize=8, color='#F0AFA8', label='API' if i == 0 else "")
    ax1.bar(x[i] + width/2, web_means, width, yerr=web_errors, capsize=8, color='#C0DAF2', label='Web' if i == 0 else "")
    x_labels.extend([f'{dataset}'])

# Setting Times New Roman font for all labels
plt.rc('font', family='Times New Roman')
ax1.set_xticks(x)
ax1.set_xticklabels(x_labels, rotation=0, ha='center', fontsize=10,family='Times New Roman')
ax1.set_ylabel('Invalid Classification State Probability', fontsize=18, family='Times New Roman')
ax1.set_ylim(0.95, 1.05)  # Adjusted y-axis range for better visibility

# Adding a second y-axis for the line plot
ax2 = ax1.twinx()
ax2.plot(x, api_means_list, marker='o', color='#EF7A6D', label='API Mean', linewidth=4)
ax2.plot(x, web_means_list, marker='o', color='#9DC3E7', label='Web Mean', linewidth=4)
ax2.set_ylim(0, 1.1)  # Make sure the line plot y-axis range matches the bar plot y-axis range

# Adding legends for both plots
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
handles = handles1 + handles2
labels = labels1 + labels2

fig.legend(handles, labels, fontsize=12, loc='upper right', bbox_to_anchor=(1, 1), ncol=1, prop={'family': 'Times New Roman'})

fig.suptitle('Comparison of Invalid Classification State Probability for Each Dataset between API and Web Methods', fontsize=22, family='Times New Roman')
plt.grid(False)  # Remove grid lines
plt.tight_layout()
plt.show()
