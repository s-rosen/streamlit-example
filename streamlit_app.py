import streamlit as st
import json
import pandas as pd
import numpy as np

json_objects = [
    {
        
        "utterances": [
            {"Utterance1": "Create a subflow that iterates through every incident record, logs it, and sends a teams message with a short description of the incident.",
             "Utterance2": "Make a subflow where for each open incident you create a detailed log entry and send it in a teams message."
            }          
        ], 
        "trigger": "null",
        "components": [
            {
                "category": "action",
                "definition": "look_up_records",
                "scope": "global",
                "order": 1
            }, 
            {
                "category": "flowlogic",
                "definition": "FOREACH",
                "scope": "global",
                "order": 2
            },
            {
                "category": "action",
                "definition": "log",
                "scope": "global",
                "order": 3,
                "block": 2
            },
            {
                "category": "action",
                "definition": "post_a_message",
                "scope": "sn_ms_teams_ah",
                "order": 4,
                "block": 2
            }   
        ]
    },
    {
        "utterances": [
            {"Utterance1": "On Mondays, go through each case and create a log.",
            "Utterance2": "Make a weekly flow that runs on Monday that checks and logs all risk management assessments performed over the week, so they could be analyzed later for any discrepancies or inconsistencies."
            }
        ],
        "trigger": {
            "type": "weekly",
            "inputs": [
                {
                    "name": "time",
                    "value": "1970-01-01 00:00:00"
                },
                {
                    "name": "day_of_week",
                    "value": "1"
                }
            ]
        },
        "components": [
            {
                "category": "action",
                "definition": "look_up_records",
                "scope": "global",
                "order": 1
            },
            {
                "category": "flowlogic",
                "definition": "FOREACH",
                "scope": "global",
                "order": 2
            },
            {
                "category": "action",
                "definition": "log",
                "scope": "global",
                "order": 3,
                "block": 2
            }
        ]
    }
]
# Initialize session state for search query and filters if not present
if 'search_query' not in st.session_state:
    st.session_state['search_query'] = ""

if 'filters' not in st.session_state:
    st.session_state.filters = {"component_definition": [], "component_category": [], "trigger_type": []}

# Sidebar for filtering based on component definitions, categories, and trigger types
st.sidebar.header("Filter options")
filter_keys = ["component_definition", "component_category", "trigger_type"]

# Generate and update filters based on user selection
for filter_key in filter_keys:
    # Assuming each JSON object's structure allows extraction of these properties
    unique_values = set()
    for obj in json_objects:
        for comp in obj.get("components", []):
            if filter_key in comp:
                unique_values.add(comp[filter_key])
    unique_values = list(unique_values)
    unique_values.sort()

    selected_filters = st.sidebar.multiselect(f"Select {filter_key.replace('_', ' ').title()}", unique_values, key=f"select_{filter_key}")
    st.session_state.filters[filter_key] = selected_filters

# Text input for search query
search_query = st.text_input("Search JSONs", value=st.session_state['search_query'])
st.session_state['search_query'] = search_query.lower()

# Function to filter JSON objects based on the search query and sidebar filters
def filter_json_objects(json_objects, query, filters):
    filtered_objects = []
    for obj in json_objects:
        json_str = json.dumps(obj).lower()
        if query in json_str:
            # Additional logic to apply sidebar filters
            match = True
            for filter_key, selected_values in filters.items():
                if selected_values:  # If there are filters to apply
                    # Custom logic to check if obj matches the filter criteria
                    # This is a placeholder and should be replaced with actual filtering logic
                    match = False
                    break
            if match:
                filtered_objects.append(obj)
    return filtered_objects

# Apply filters
filtered_json_objects = filter_json_objects(json_objects, st.session_state['search_query'], st.session_state.filters)

# Display filtered JSON objects
st.write(f"Filtered JSON Objects ({len(filtered_json_objects)} found):")
for index, json_obj in enumerate(filtered_json_objects):
    with st.expander(f"JSON {index + 1}"):
        st.json(json_obj)