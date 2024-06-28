import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the uploaded CSV file
file_path = "E:/Evaluate_results_for_all_datasets/Evaluate_table/Quantity/quantity_redundancies.csv"
data = pd.read_csv(file_path)

# Rename columns for clarity
data.columns = ['Dataset', 'API1', 'API2', 'API3', 'API4', 'API5']

# Remove the row with 'Dataset/time'
data = data[data['Dataset'] != 'Dataset/time']

# Convert the data into a long format suitable for plotting a stacked bar chart
data_long = data.melt(id_vars='Dataset', var_name='API', value_name='Redundancies')

# Convert 'Redundancies' column to numeric, coercing errors to NaN and then filling them with 0
data_long['Redundancies'] = pd.to_numeric(data_long['Redundancies'], errors='coerce').fillna(0)

# Set seaborn style
sns.set(style="white")

# Set font to Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# Custom color palette
scatter_palette = [
    '#FF9999', '#FFB3B3', '#FFCCCC', '#FFD9D9', '#FFE5E5',  # Light red
    '#9DC3E7', '#AED8F0', '#ADD8E6','#BFECF9', '#D0F0FF', '#E0F7FF'   # Light blue
]

# Plotting the horizontal stacked bar chart
plt.figure(figsize=(14, 6))
data_pivot = data_long.pivot(index='Dataset', columns='API', values='Redundancies')

# Increase bar width by decreasing the gap between bars
bar_width = 0.75  # You can adjust this value to make bars thicker or thinner
ax = data_pivot.plot(kind='barh', stacked=True, color=scatter_palette[:len(data_pivot.columns)], edgecolor='grey', width=bar_width)

# Add data labels
for bars in ax.containers:
    ax.bar_label(bars, labels=[f'{int(label)}' if label > 0 else '' for label in bars.datavalues],
                 label_type='center', fontsize=12, color='grey', fontweight='bold')

# Set labels and title
plt.xlabel('Redundancies number', fontsize=12)
plt.ylabel('Dataset', fontsize=12)
plt.title('Redundancies in Taxonomic Keys across Different API Runs', fontsize=14)

# Adjust legend position
plt.legend(title='API', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

# Make axes more prominent
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.5)
ax.spines['bottom'].set_linewidth(1.5)
ax.xaxis.label.set_size(12)
ax.yaxis.label.set_size(12)
ax.tick_params(axis='x', which='major', labelsize=10, length=6, width=2, direction='out', color='black')
ax.tick_params(axis='y', which='major', labelsize=10, length=6, width=2, direction='out', color='black')

# Add tick lines on the X-axis and Y-axis, only on the bottom and left
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.tick_params(axis='x', direction='out', length=5, width=1, colors='black')
ax.tick_params(axis='y', direction='out', length=5, width=1, colors='black')

plt.tight_layout()
plt.show()
