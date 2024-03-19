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
# Initialize session state
if 'filters' not in st.session_state:
    st.session_state.filters = {"component_definition": [], "component_category": [], "trigger_type": []}
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

# Sidebar for filtering
st.sidebar.header("Filter options")
filter_keys = ["component_definition", "component_category", "trigger_type"]
filter_key = st.sidebar.radio("Filter by", options=filter_keys)

# Generate a list of unique values for the selected filter key
# This requires the DataFrame `df` to be defined with these columns
# Ensure the DataFrame creation logic is placed correctly and includes these keys

# Dummy DataFrame creation for demonstration; replace with your actual data processing logic
df = pd.DataFrame({
    "json_index": np.arange(len(json_objects)),
    "component_definition": ["def1", "def2"],
    "component_category": ["cat1", "cat2"],
    "trigger_type": ["type1", "type2"],
})

unique_values = df[filter_key].dropna().unique().tolist()
unique_values = [str(value) for value in unique_values]
unique_values.sort()

selected_filters = st.sidebar.multiselect("Select {}".format(filter_key), unique_values, key=filter_key)
st.session_state.filters[filter_key] = selected_filters

# Text input for search functionality, ensuring it updates on enter
search_query = st.text_input("Search JSONs", key='search_query', on_change=lambda: st.session_state.update({'search_query': st.session_state.search_query}))

# Filter logic here
# Adjust this to match your actual data structure and filtering needs
filtered_indices = set(df.index)
for key in filter_keys:
    if st.session_state.filters.get(key):
        filtered_indices &= set(df[df[key].isin(st.session_state.filters[key])].index)

if st.session_state.search_query:
    filtered_indices &= set(df[df.apply(lambda row: st.session_state.search_query.lower() in json.dumps(row.to_dict()).lower(), axis=1)].index)

filtered_json_indices = [int(index) for index in filtered_indices]  # Ensure indices are integers

# Display filtered JSONs
st.write("Filtered JSON Objects:")
for index in filtered_json_indices:
    with st.expander(f"JSON {index + 1}"):
        st.json(json_objects[index])
