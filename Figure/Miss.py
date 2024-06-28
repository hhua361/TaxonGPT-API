import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter

# Load the new CSV file
file_path = "E:/Evaluate_results_for_all_datasets/Evaluate_table/Quantity/quantity_miss.csv"
data_new = pd.read_csv(file_path)

# Rename columns for clarity
data_new.columns = ['Dataset', 'API1', 'API2', 'API3', 'API4', 'API5', 'Web1', 'Web2', 'Web3', 'Web4', 'Web5']

# Remove the row with 'Dataset/time'
data_new = data_new[data_new['Dataset'] != 'Dataset/time']

# Convert all the values to numeric and handle any potential non-numeric issues
for col in data_new.columns[1:]:
    data_new[col] = pd.to_numeric(data_new[col], errors='coerce').fillna(0)

# Convert the data into a long format suitable for plotting a stacked bar chart
data_long_new = data_new.melt(id_vars='Dataset', var_name='Method', value_name='Miss-rate')

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
plt.figure(figsize=(14, 8))  # Adjust the figure size
data_pivot_new = data_long_new.pivot(index='Dataset', columns='Method', values='Miss-rate')

# Increase bar width by decreasing the gap between bars
bar_width = 0.85  # You can adjust this value to make bars thicker or thinner
ax = data_pivot_new.plot(kind='barh', stacked=True, color=scatter_palette[:len(data_pivot_new.columns)], edgecolor='grey', width=bar_width)

# Add data labels only at specified positions to avoid overlap
for bars in ax.containers:
    for bar, label in zip(bars, bars.datavalues):
        method = bars.get_label()
        if label > 0:
            if method == 'API3' and label == 0.053:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, f'{label:.1%}',
                        ha='center', va='center', fontsize=10, color='grey')
            elif method == 'API4' and label == 0.041:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, f'{label:.1%}',
                        ha='center', va='center', fontsize=10, color='grey')
            elif label not in [0.053, 0.041]:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, f'{label:.1%}',
                        ha='center', va='center', fontsize=10, color='grey')

# Set labels and title
plt.xlabel('Missed Species Percentage', fontsize=12)
plt.ylabel('Dataset', fontsize=12)
plt.title('Missed Species Percentage in Taxonomic Keys across Different Methods', fontsize=14)

# Adjust legend position
plt.legend(title='Method', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

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

# Set the x-axis to percentage
ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))

plt.tight_layout()
plt.show()
