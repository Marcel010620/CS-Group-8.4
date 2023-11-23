import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define your data
data = {'Article': ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'],
        'Quantity': [10, 5, 7, 3, 2],
        'Category': ['Fruit', 'Fruit', 'Fruit', 'Fruit', 'Fruit']}

df = pd.DataFrame(data)

# Sort data by quantity in descending order
df = df.sort_values(by='Quantity', ascending=False)
df = df.reset_index(drop=True)  # Reset the index for correct bar positioning

# Set figure size
fig, ax = plt.subplots(figsize=(10, 5))

# Set the color of the bar for each category
color_dict = {'Fruit': 'c'}

# Define bar positions on x axis
bar_positions = range(len(df['Article']))

# Create bars with small spaces
bar_width = 0.8  # Adjust the width as needed
for i, row in df.iterrows():
    ax.bar(bar_positions[i], row['Quantity'], color=color_dict[row['Category']], alpha=0.6, width=bar_width)

# Set axes limits
ax.set_ylim(0, df['Quantity'].max() + 2)

# Add labels above the bars
for i, row in df.iterrows():
    ax.text(bar_positions[i], row['Quantity'] + 0.2, row['Article'], fontsize=12, ha='center')

# Remove x-axis labels below the axis
ax.set_xticks([])
ax.set_xticklabels([])

# Display the plot using Streamlit
st.pyplot(fig)
