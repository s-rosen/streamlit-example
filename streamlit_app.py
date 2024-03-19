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

if 'component_definition' not in st.session_state:
    st.session_state['component_definition'] = []

if 'component_category' not in st.session_state:
    st.session_state['component_category'] = []

# Extract unique values for component_definition and component_category
unique_definitions = set()
unique_categories = set()
for obj in json_objects:
    for component in obj.get("components", []):
        unique_definitions.add(component.get("definition"))
        unique_categories.add(component.get("category"))

# Sidebar for filtering based on component definitions and categories
st.sidebar.header("Filter options")
selected_definitions = st.sidebar.multiselect("Select Component Definition", list(unique_definitions), key="select_component_definition")
selected_categories = st.sidebar.multiselect("Select Component Category", list(unique_categories), key="select_component_category")

# Update the session state for filters
st.session_state['component_definition'] = selected_definitions
st.session_state['component_category'] = selected_categories

# Text input for search query
search_query = st.text_input("Search JSONs", value=st.session_state['search_query'])
st.session_state['search_query'] = search_query.lower()

# Function to filter JSON objects based on the search query and selected filters
def filter_json_objects(json_objects, query, selected_definitions, selected_categories):
    filtered_objects = []
    for obj in json_objects:
        json_str = json.dumps(obj).lower()
        definitions_match = all(defi in json_str for defi in map(str.lower, selected_definitions))
        categories_match = all(cat in json_str for cat in map(str.lower, selected_categories))
        if query in json_str and definitions_match and categories_match:
            filtered_objects.append(obj)
    return filtered_objects

# Apply filters
filtered_json_objects = filter_json_objects(json_objects, st.session_state['search_query'], st.session_state['component_definition'], st.session_state['component_category'])

# Display filtered JSON objects
st.write(f"Filtered JSON Objects ({len(filtered_json_objects)} found):")
for index, json_obj in enumerate(filtered_json_objects):
    with st.expander(f"JSON {index + 1}"):
        st.json(json_obj)