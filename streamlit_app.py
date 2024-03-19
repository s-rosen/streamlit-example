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

# Initialize session state for search query and filters if not already set
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

if 'filters' not in st.session_state:
    st.session_state.filters = {"component_definition": [], "component_category": [], "trigger_type": []}

# Text input for the search functionality
search_query = st.text_input("Search JSONs", value=st.session_state.search_query)
st.session_state.search_query = search_query

# Preprocess JSON objects to create a DataFrame for filtering
flattened_data = []
for index, obj in enumerate(json_objects):
    trigger_type = obj.get("trigger", {}).get("type", "None") if isinstance(obj.get("trigger", {}), dict) else "None"
    for component in obj.get("components", []):
        flattened_data.append({
            "json_index": index,
            "component_definition": component.get("definition", "None"),
            "component_category": component.get("category", "None"),
            "trigger_type": trigger_type,
        })

df = pd.DataFrame(flattened_data)

# Sidebar for filtering options
st.sidebar.header("Filter options")
filter_keys = ["component_definition", "component_category", "trigger_type"]
filter_key = st.sidebar.radio("Filter by", options=filter_keys)

# Generate a list of unique values for the selected filter key, ensuring all values are strings for sorting
unique_values = df[filter_key].dropna().unique()
unique_values = [str(value) for value in unique_values]  # Convert all to strings to ensure sorting works
unique_values.sort()

selected_filters = st.sidebar.multiselect("Select {filter_key}", unique_values)

# Update filters based on selection
st.session_state.filters[filter_key] = selected_filters

# Apply filters to DataFrame
def apply_filters(df, filters, search_query):
    filtered_df = df.copy()
    for key, values in filters.items():
        if values:
            filtered_df = filtered_df[filtered_df[key].isin(values)]
    if search_query:
        search_query = search_query.lower()  # Case-insensitive search
        filtered_df = filtered_df[filtered_df.apply(lambda row: search_query in json.dumps(row.to_dict()).lower(), axis=1)]
    return filtered_df

filtered_df = apply_filters(df, st.session_state.filters, st.session_state.search_query)

# Display filtered JSON objects as expandable items
st.write("Filtered JSON Objects:")
filtered_indices = filtered_df['json_index'].drop_duplicates().to_numpy(dtype=int)
for i in filtered_indices:
    with st.expander(f"JSON {i + 1}"):
        st.json(json_objects[i])
