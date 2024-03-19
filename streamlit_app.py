import streamlit as st
import json
import pandas as pd

# Example list of JSON objects. Replace this with your actual JSON objects or the method to load/fetch them.
json_objects = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "San Francisco"},
    {"name": "Charlie", "age": 35, "city": "London"},
    {"name": "Alice", "age": 35, "city": "Cairo"},
    {"name": "Bob", "age": 80, "city": "Paris"},
    {"name": "Charlie", "age": 6, "city": "Tokyo"}
]

# Convert JSON objects to strings for display
json_strings = [json.dumps(obj, indent=2) for obj in json_objects]


# Initialize the toggle state in Streamlit's session state if it's not already set
if 'show_json_editor' not in st.session_state:
    st.session_state.show_json_editor = False

# Button to toggle the visibility of the JSON editor
if st.button("Edit JSON"):
    # Flip the current state
    st.session_state.show_json_editor = not st.session_state.show_json_editor

# Conditionally show the text area based on the toggle state
if st.session_state.show_json_editor:
    st.text_area("JSON String", value=json_strings[selected_index], height=300)

# Convert the list of JSONs to a DataFrame for easier handling
df = pd.DataFrame(json_objects)

# Sidebar for filtering
st.sidebar.header("Filter options")
filter_key = st.sidebar.selectbox("Filter by", options=["name", "age", "city"])

# Generate a list of unique values for the selected filter key
unique_values = df[filter_key].unique().tolist()
unique_values.sort()  # Optional: sort the list for easier browsing

# Use a selectbox (for single selection) or multiselect (for multiple selections) for the filter values
# For a single selection:
filter_value = st.sidebar.selectbox(f"Select {filter_key}", [''] + unique_values)

# For multiple selections (optional alternative):
# filter_value = st.sidebar.multiselect(f"Select {filter_key}", unique_values)

# Filter the DataFrame based on the selected filter_key and filter_value
if filter_value:
    if isinstance(filter_value, list):  # If using multiselect
        filtered_df = df[df[filter_key].isin(filter_value)]
    else:  # If using selectbox
        filtered_df = df[df[filter_key] == filter_value]
else:
    filtered_df = df

# Display filtered JSONs
if not filtered_df.empty:
    selected_index = st.selectbox("Select an entry", range(len(filtered_df)), format_func=lambda x: f"{filtered_df.iloc[x]['name']} - {filtered_df.iloc[x]['age']} - {filtered_df.iloc[x]['city']}")
    if st.button("Display JSON"):
        st.json(filtered_df.iloc[selected_index].to_dict())
else:
    st.write("No entries match your filter criteria.")

# Display filtered JSONs
selected_index = st.selectbox("Select an entry", range(len(filtered_df)), format_func=lambda x: filtered_df.iloc[x]["name"])
st.json(filtered_df.iloc[selected_index].to_dict())
