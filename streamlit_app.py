import streamlit as st
import json

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
