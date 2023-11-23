
!pip install matplotlib
!pip list
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


import streamlit as st
from datetime import datetime, timedelta

# Initialize session state
if "selected_options" not in st.session_state:
    st.session_state.selected_options = {"Article": None, "Owner": None, "show_select_boxes": {"add_item_button": False, "remove_item_button": False, "add_owner_button": False, "remove_owner_button": False}}

# Insert the name of the fridge (for example, your WG Name)
wg_name = st.text_input("Your WG name")

# Display the title with the correct name given by a user input
st.markdown(f"# This is the smart refrigerator of: <span style='color:red;'>{wg_name}</span>", unsafe_allow_html=True)

# Initialize 4 columns to order 4 buttons in a row
col1, col2, col3, col4 = st.columns(4)

# What happens if you press the add_item_button
add_item_button = col1.button("Add product")
if add_item_button:
    st.session_state.selected_options["show_select_boxes"]["add_item_button"] = True
    # Reset other buttons
    st.session_state.selected_options["show_select_boxes"]["remove_item_button"] = False
    st.session_state.selected_options["show_select_boxes"]["add_owner_button"] = False
    st.session_state.selected_options["show_select_boxes"]["remove_owner_button"] = False

# What happens if you press the remove_item_button
remove_item_button = col2.button("Remove product")
if remove_item_button:
    st.session_state.selected_options["show_select_boxes"]["remove_item_button"] = True
    # Reset other buttons
    st.session_state.selected_options["show_select_boxes"]["add_item_button"] = False
    st.session_state.selected_options["show_select_boxes"]["add_owner_button"] = False
    st.session_state.selected_options["show_select_boxes"]["remove_owner_button"] = False

# What happens if you press the add_owner_button
add_owner_button = col3.button("Add owners")
if add_owner_button:
    st.session_state.selected_options["show_select_boxes"]["add_owner_button"] = True
    # Reset other buttons
    st.session_state.selected_options["show_select_boxes"]["add_item_button"] = False
    st.session_state.selected_options["show_select_boxes"]["remove_item_button"] = False
    st.session_state.selected_options["show_select_boxes"]["remove_owner_button"] = False

# What happens if you press the remove_owner_button
remove_owner_button = col4.button("Remove owner")
if remove_owner_button:
    st.session_state.selected_options["show_select_boxes"]["remove_owner_button"] = True
    # Reset other buttons
    st.session_state.selected_options["show_select_boxes"]["add_item_button"] = False
    st.session_state.selected_options["show_select_boxes"]["remove_item_button"] = False
    st.session_state.selected_options["show_select_boxes"]["add_owner_button"] = False

# Show select boxes if the flag is True
if st.session_state.selected_options["show_select_boxes"]["add_item_button"]:
    options_Article = ["Pepper", "Milk"]
    st.session_state.selected_options["Article"] = st.selectbox("Choose your Article", options_Article,
                                                                key="article_selectbox")
    st.write('You selected:', st.session_state.selected_options["Article"])

    options_Owner = ["A", "B", "C"]
    st.session_state.selected_options["Owner"] = st.selectbox("Choose the Owner", options_Owner,
                                                              key="owner_selectbox")
    st.write("You selected", st.session_state.selected_options["Owner"])

# Show select boxes if the flag is True
if st.session_state.selected_options["show_select_boxes"]["remove_item_button"]:
    remove_options_article = ["Pepper", "Milk"]  # This needs to be a list with all Products inside the fridge
    removed_options_article = st.selectbox("Choose the articles you want to remove", remove_options_article)
    st.write("You removed", removed_options_article)

# Show select boxes if the flag is True
if st.session_state.selected_options["show_select_boxes"]["add_owner_button"]:
    new_owner = st.text_input("Enter new owner")
    if new_owner:
        st.session_state.selected_options["Owner"] = new_owner
        st.write("New owner added:", new_owner)

# Show select boxes if the flag is True
if st.session_state.selected_options["show_select_boxes"]["remove_owner_button"]:
    owners_list = ["A", "B", "C"]  # Replace with your list of owners
    removed_owner = st.selectbox("Choose the owner to remove", owners_list)
    if removed_owner:
        st.session_state.selected_options["Owner"] = None
        st.write("Removed owner:", removed_owner)
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

# Define bar positions on x-axis
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

# Close the Matplotlib figure to clear it from memory
plt.close(fig)