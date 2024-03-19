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

if 'trigger_type' not in st.session_state:
    st.session_state['trigger_type'] = []

if 'number_of_components' not in st.session_state:
    st.session_state['number_of_components'] = []

# Sidebar for filtering based on component definitions, categories, trigger types, and number of components
st.sidebar.header("Filter options")

# Extract unique values for filters
unique_definitions = set()
unique_categories = set()
unique_triggers = set()
component_counts = set()

for obj in json_objects:
    for component in obj.get("components", []):
        unique_definitions.add(component.get("definition", "Unknown"))
        unique_categories.add(component.get("category", "Unknown"))
    trigger = obj.get("trigger")
    if isinstance(trigger, dict):
        unique_triggers.add(trigger.get("type", "Unknown"))
    else:
        unique_triggers.add("Unknown" if trigger is None else str(trigger))
    component_counts.add(len(obj.get("components", [])))

# Convert sets to sorted lists
unique_definitions = sorted(list(unique_definitions))
unique_categories = sorted(list(unique_categories))
unique_triggers = sorted(list(unique_triggers))
component_counts = sorted(list(component_counts))

# Filter UI
selected_definitions = st.sidebar.multiselect("Component Definition", unique_definitions, key="filter_component_definition")
st.session_state['component_definition'] = selected_definitions

selected_categories = st.sidebar.multiselect("Component Category", unique_categories, key="filter_component_category")
st.session_state['component_category'] = selected_categories

selected_triggers = st.sidebar.multiselect("Trigger Type", unique_triggers, key="filter_trigger_type")
st.session_state['trigger_type'] = selected_triggers

selected_component_count = st.sidebar.multiselect("Number of Components", component_counts, key="filter_number_of_components")
st.session_state['number_of_components'] = selected_component_count

# Text input for search query
search_query = st.text_input("Search JSONs", value=st.session_state['search_query'])
st.session_state['search_query'] = search_query.lower()

# Function to filter JSON objects based on the search query and selected filters
def filter_json_objects(json_objects, query, session_state):
    filtered_objects = []
    for obj in json_objects:
        # Serialize object and search
        if query not in json.dumps(obj).lower():
            continue

        # Apply additional filter logic
        components = obj.get("components", [])
        if (selected_definitions and not any(comp.get("definition") in selected_definitions for comp in components)) or \
           (selected_categories and not any(comp.get("category") in selected_categories for comp in components)) or \
           (selected_triggers and (str(obj.get("trigger")) not in selected_triggers and obj.get("trigger", {}).get("type") not in selected_triggers)) or \
           (selected_component_count and len(components) not in selected_component_count):
            continue
        
        filtered_objects.append(obj)
    
    return filtered_objects

# Apply filters and search
filtered_json_objects = filter_json_objects(json_objects, st.session_state['search_query'], st.session_state)

# Display filtered JSON objects
st.write(f"Filtered JSON Objects ({len(filtered_json_objects)} found):")
for index, json_obj in enumerate(filtered_json_objects):
    with st.expander(f"JSON {index + 1}"):
        st.json(json_obj)