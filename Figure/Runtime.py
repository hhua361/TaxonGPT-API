import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
data_file_path = "D:/桌面/Processed_Test_Extract_Matrix.xlsx"
data = pd.read_excel(data_file_path)

# Extract character numbers and accuracy values for each trial
character_numbers = data.iloc[:, 0]  # X-axis: Character numbers
accuracy_values = data.iloc[:, 1:21]  # Y-axis: Accuracy values for 20 trials

# Calculate the mean and standard deviation for each character number
means = accuracy_values.mean(axis=1)
std_devs = accuracy_values.std(axis=1)

# Create the scatter plot
plt.figure(figsize=(12, 8))

# Plot error bars showing the standard deviation for each character number
plt.errorbar(character_numbers, means, yerr=std_devs, fmt='o', capsize=5,
             label='Average value ± Standard Deviation', color='#5F97D2', ecolor='#5F97D2', elinewidth=2, capthick=2)

# Plot the average values as scatter points
plt.scatter(character_numbers, means, color='#D76364', label='Average value', s=100, zorder=5)

# Plot the trend line connecting the average values
plt.plot(character_numbers, means, color='#EF7A6D', label='Trend Line', linewidth=2)

# Scatter the individual trial points with a small random offset
offset = np.random.uniform(-0.8, 0.8, size=accuracy_values.shape)  # Larger range of offset
for i in range(accuracy_values.shape[1]):
    plt.scatter(character_numbers + offset[:, i], accuracy_values.iloc[:, i], alpha=0.5, color='gray')

# Remove the right and top spines (axes lines)
ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Adjust the font size of the axis ticks
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

# Set the title and labels
plt.title('The effect of extract accuracy with Character Number', fontsize=20)
plt.xlabel('Character Number', fontsize=18)
plt.ylabel('Accuracy (%)', fontsize=18)

# Add legend with adjusted position
plt.legend(fontsize=14, loc='upper left', bbox_to_anchor=(1.05, 1))  # 将图注右移

# Show the plot
plt.show()

