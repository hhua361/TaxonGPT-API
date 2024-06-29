import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Load the updated CSV file
file_path = "E:/Evaluate_results_for_all_datasets/Evaluate_table/Accuarcy/accuracy.csv"  # 你需要将文件路径更新为你的文件路径
updated_accuracy_data = pd.read_csv(file_path)

# Data preprocessing to convert percentage strings to numeric values
def convert_percentage_to_numeric(percentage):
    if isinstance(percentage, str):
        if '%' in percentage:
            return float(percentage.strip('%'))
        else:
            try:
                return float(percentage)
            except ValueError:
                return 100.0  # Default to 100 if the value is invalid or missing
    return 100.0

# Convert all relevant columns
for col in updated_accuracy_data.columns[1:]:
    updated_accuracy_data[col] = updated_accuracy_data[col].apply(convert_percentage_to_numeric)

# Extracting relevant columns for API and Web accuracies
api_columns = [col for col in updated_accuracy_data.columns if 'API' in col]
web_columns = [col for col in updated_accuracy_data.columns if 'Web' in col]

# Calculating the average accuracy for API and Web methods
heatmap_data = updated_accuracy_data.set_index('Unnamed: 0')
heatmap_data['API Average'] = heatmap_data[api_columns].mean(axis=1)
heatmap_data['Web Average'] = heatmap_data[web_columns].mean(axis=1)

# Creating a new DataFrame with average accuracies
average_accuracy_data = heatmap_data[['API Average', 'Web Average']]

# Define a custom color map with the specified color
colors = ["#DFEEFB", "#C0DAF2"]  # white to the specified color
custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)

# Plotting the heatmap for average accuracies with the custom color map
plt.figure(figsize=(14, 8))  # 调整图像大小以确保内容显示完整

# Create the heatmap with the colorbar
ax = sns.heatmap(average_accuracy_data, annot=False, cmap=custom_cmap, cbar_kws={'shrink': 0.8, 'aspect': 20})
cbar = ax.collections[0].colorbar

# Adjust colorbar tick labels
cbar.ax.tick_params(labelsize=16, labelcolor='black')
cbar.ax.set_yticklabels(cbar.ax.get_yticklabels(), fontsize=16, fontname='Times New Roman')

# Add colorbar label using annotate to precisely control the position
ax.annotate('Accuracy (%)', xy=(1.02, 0.95), xycoords='axes fraction', fontsize=18, fontname='Times New Roman', annotation_clip=False)

# Custom annotation function to add '%' symbol to the heatmap annotations and remove decimal places for 100%
def annotate_heatmap(data, annot_data, fmt=".2f", textsize=14, textfont='Times New Roman'):
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            value = annot_data[i, j]
            if value == 100:
                plt.text(j + 0.5, i + 0.5, f"{int(value)}%", ha='center', va='center', color='black', fontsize=textsize, fontname=textfont)
            else:
                plt.text(j + 0.5, i + 0.5, f"{value:{fmt}}%", ha='center', va='center', color='black', fontsize=textsize, fontname=textfont)

# Add annotations after the heatmap is created
annotate_heatmap(average_accuracy_data.values, average_accuracy_data.values, textsize=18, textfont='Times New Roman')

# Adjust title position
plt.title('Average Classification Accuracy Comparison between API and Web Methods across Datasets', fontsize=22, fontname='Times New Roman', pad=20)
plt.xlabel('Methods', fontsize=18, fontname='Times New Roman')
plt.ylabel('Datasets', fontsize=18, fontname='Times New Roman')

plt.xticks(fontsize=16, fontname='Times New Roman')
plt.yticks(fontsize=16, fontname='Times New Roman')

# Add bottom and left spines and adjust their thickness
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.spines['bottom'].set_linewidth(2)  # Adjust the thickness here
ax.spines['left'].set_linewidth(2)    # Adjust the thickness here

# Adjust tick parameters for x and y axis
ax.tick_params(axis='x', which='both', bottom=True, top=False, labelbottom=True, direction='out', length=6, width=2)
ax.tick_params(axis='y', which='both', left=True, right=False, labelleft=True, direction='out', length=6, width=2)

plt.tight_layout()  # 调整布局以确保内容显示完整
plt.show()
