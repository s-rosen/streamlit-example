import streamlit as st
import json
import pandas as pd

# Example list of JSON objects. Replace this with your actual JSON objects or the method to load/fetch them.
json_objects = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "San Francisco"},
    {"name": "Charlie", "age": 35, "city": "London"}
]

# Convert JSON objects to strings for display
json_strings = [json.dumps(obj, indent=2) for obj in json_objects]

# Sidebar for selecting which JSON to display
selected_index = st.sidebar.selectbox("Select JSON", range(len(json_strings)), format_func=lambda x: f"JSON {x + 1}")

# Display the selected JSON
st.json(json_objects[selected_index])

# Optionally, display the JSON string in a text area (read-only)
st.text_area("JSON String", json_strings[selected_index], height=300)

# Convert the list of JSONs to a DataFrame for easier handling
df = pd.DataFrame(data)

# Sidebar for filtering
st.sidebar.header("Filter options")
filter_key = st.sidebar.selectbox("Filter by", options=["name", "age", "city"])
filter_value = st.sidebar.text_input(f"Enter {filter_key}")

# Filter the DataFrame based on the selected filter_key and filter_value
if filter_value:
    filtered_df = df[df[filter_key].astype(str).str.contains(filter_value, case=False)]
else:
    filtered_df = df

# Display filtered JSONs
selected_index = st.selectbox("Select an entry", range(len(filtered_df)), format_func=lambda x: filtered_df.iloc[x]["name"])
if st.button("Display JSON"):
    st.json(filtered_df.iloc[selected_index].to_dict())
