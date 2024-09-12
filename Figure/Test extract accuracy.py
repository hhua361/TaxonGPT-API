
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data_file_path = "D:/桌面/111.xlsx"
data = pd.read_excel(data_file_path)

# Extract character numbers and accuracy values
character_numbers = data['Character number']  # X-axis: Character numbers
accuracy_values = data['Accurcy']  # Y-axis: Accuracy values (average)

# Create the plot
plt.figure(figsize=(12, 8))

# Plot the accuracy values as a line plot with connected points
plt.plot(character_numbers, accuracy_values, color='#5F97D2', label='Trend Line', zorder=1)  # Blue line

# Plot the scatter points
plt.scatter(character_numbers, accuracy_values, color='#D76364', label='Average Accuracy', zorder=2)  # Red scatter points

# Remove the right and top spines (axes lines)
ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Adjust the font size of the axis ticks
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

# Set the title and labels
plt.title('Accuracy vs. Character Number', fontsize=20)
plt.xlabel('Character Number', fontsize=18)
plt.ylabel('Accuracy (%)', fontsize=18)

# Add legend
plt.legend()

# Save the plot as an SVG file
plt.savefig("D:/桌面/Accuracy_vs_Character_Number_(API).png", format='png')

# Show the plot
plt.show()

