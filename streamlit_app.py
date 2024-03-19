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

# Initialize filter states
filter_keys = ['component_definition', 'component_category', 'trigger_type', 'num_components']
for key in filter_keys:
    if key not in st.session_state:
        st.session_state[key] = []

# Sidebar for filtering
st.sidebar.header("Filter options")

# Extract unique values for filters dynamically from json_objects
unique_definitions = set()
unique_categories = set()
unique_triggers = set()
num_components_options = set()

for obj in json_objects:
    for component in obj.get("components", []):
        unique_definitions.add(component.get("definition"))
        unique_categories.add(component.get("category"))
    # Handle trigger type
    if isinstance(obj.get("trigger"), dict):
        unique_triggers.add(obj["trigger"].get("type"))
    else:
        unique_triggers.add(obj.get("trigger"))  # Direct string or null
    # Count components
    num_components_options.add(len(obj.get("components", [])))

# Multiselect for component definitions
selected_definitions = st.sidebar.multiselect("Select Component Definition", list(unique_definitions), key="select_component_definition")

# Multiselect for component categories
selected_categories = st.sidebar.multiselect("Select Component Category", list(unique_categories), key="select_component_category")

# Multiselect for trigger types
selected_triggers = st.sidebar.multiselect("Select Trigger Type", list(unique_triggers), key="select_trigger_type")

# Multiselect for number of components
selected_num_components = st.sidebar.multiselect("Select Number of Components", sorted(list(num_components_options)), key="select_num_components")

# Update session state for filters
st.session_state['component_definition'] = selected_definitions
st.session_state['component_category'] = selected_categories
st.session_state['trigger_type'] = selected_triggers
st.session_state['num_components'] = selected_num_components

# Text input for search query
search_query = st.text_input("Search JSONs", value=st.session_state['search_query'])
st.session_state['search_query'] = search_query.lower()

# Function to filter JSON objects
def filter_json_objects(json_objects, query, filters):
    filtered_objects = []
    for obj in json_objects:
        json_str = json.dumps(obj).lower()
        if query in json_str:
            # Additional checks for each filter type
            definitions_match = all(defi in json_str for defi in map(str.lower, filters['component_definition']))
            categories_match = all(cat in json_str for cat in map(str.lower, filters['component_category']))
            triggers_match = (obj.get("trigger", {}).get("type", "") in filters['trigger_type']) or (str(obj.get("trigger")) in filters['trigger_type'])
            num_components_match = (len(obj.get("components", [])) in filters['num_components'])

            if definitions_match and categories_match and triggers_match and num_components_match:
                filtered_objects.append(obj)
    return filtered_objects

# Apply filters
filtered_json_objects = filter_json_objects(json_objects, st.session_state['search_query'], st.session_state)

# Display filtered JSON objects
st.write(f"Filtered JSON Objects ({len(filtered_json_objects)} found):")
for index, json_obj in enumerate(filtered_json_objects):
    with st.expander(f"JSON {index + 1}"):
        st.json(json_obj)