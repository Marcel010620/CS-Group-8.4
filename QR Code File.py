import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Define your data
data = {'Article': ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'],
        'Quantity': [10, 5, 7, 3, 2],
        'Category': ['Fruit', 'Fruit', 'Fruit', 'Fruit', 'Fruit']}

df = pd.DataFrame(data)

# Sort data by quantity in descending order
df = df.sort_values(by='Quantity', ascending=False)

# Set figure size
plt.figure(figsize=(10,5))

# Set the color of the bar for each category
color_dict = {'Fruit': 'g'}

# Define bar positions on x axis
bar_positions = range(len(df['Article']))

# Create bars
for i, row in df.iterrows():
    plt.bar(bar_positions[i], row['Quantity'], color=color_dict[row['Category']], alpha=0.6)

# Create bar labels
for i, row in df.iterrows():
    plt.text(bar_positions[i], row['Quantity'] + 0.2, row['Article'], fontsize=12)

# Set axes limits
plt.ylim(0, df['Quantity'].max() + 2)

# Create custom x-axis ticks and labels for the articles
article_ticks = []
article_labels = []

for i, row in df.iterrows():
    article_ticks.append(i + 0.5)
    article_labels.append(row['Article'])

plt.xticks(article_ticks, article_labels, rotation=90)

# Show the plot
plt.show()