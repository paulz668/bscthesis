import json
import matplotlib as plt

name = "labels.json"

with open(name, 'r') as file:
    labels = json.load(file)

plt.figure(figsize=(10, 6))

# Iterate through the keys in the 'labels' dictionary and plot a frequency plot for each list
for key, value in labels.items():
    x = [int(i) for i in value.keys()]  # Convert the keys to integers
    y1 = [value[i][0] for i in value.keys()]  # Frequency of label '1'
    y2 = [value[i][1] for i in value.keys()]  # Frequency of label '2'
    y3 = [value[i][2] for i in value.keys()]  # Frequency of label '3'

    # Plot frequency of label '1' with blue color
    plt.plot(x, y1, label=f'{key} - Label 1', color='b', marker='o')

    # Plot frequency of label '2' with green color
    plt.plot(x, y2, label=f'{key} - Label 2', color='g', marker='s')

    # Plot frequency of label '3' with red color
    plt.plot(x, y3, label=f'{key} - Label 3', color='r', marker='x')

# Set labels and title
plt.xlabel('X Values')
plt.ylabel('Frequency')
plt.title('Frequency Plots of Labels 1, 2, and 3')

# Add a legend
plt.legend()

# Show the plot
plt.grid(True)
plt.show()


