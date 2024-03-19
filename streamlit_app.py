import streamlit as st
import json
import pandas as pd

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

# Preprocess JSON objects to flatten the data for pandas
flattened_data = []
for index, obj in enumerate(json_objects):
    trigger_type = obj["trigger"]["type"] if isinstance(obj.get("trigger", {}), dict) and "type" in obj["trigger"] else "None"
    for component in obj.get("components", []):
        flattened_data.append({
            "json_index": index,
            "component_definition": component.get("definition", "None"),
            "component_category": component.get("category", "None"),
            "trigger_type": trigger_type,
        })

# Convert the preprocessed data to a DataFrame
df = pd.DataFrame(flattened_data)

# Initialize the session state for filters if it doesn't exist yet
if 'filters' not in st.session_state:
    st.session_state.filters = {"component_definition": [], "component_category": [], "trigger_type": []}
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

# Text input for search functionality
search_query = st.text_input("Search JSONs", value=st.session_state.search_query, key='search_query')

# Sidebar for filtering
st.sidebar.header("Filter options")
filter_keys = ["component_definition", "component_category", "trigger_type"]
filter_key = st.sidebar.radio("Filter by", options=filter_keys, key="filter_by_key")

# Generate a list of unique values for the selected filter key
unique_values = df[filter_key].unique().tolist()
unique_values.sort()  # Sort the list for easier browsing

# Multiselect for the filter values
selected_filters = st.sidebar.multiselect(f"Select {filter_key}", unique_values, key=f"select_{filter_key}")

# Save the selected filters and search query to the session state
st.session_state.filters[filter_key] = selected_filters
st.session_state.search_query = search_query.lower()  # Convert search query to lowercase for case-insensitive search

# Filter the DataFrame based on the selected filters
filtered_indices = set(df.index)  # Start with all indices
for key in filter_keys:
    if st.session_state.filters[key]:  # If there are any filters for this key
        filtered_indices &= set(df[df[key].isin(st.session_state.filters[key])].index)

# Apply text search to the filtered DataFrame
if st.session_state.search_query:
    filtered_indices &= set(df[df.apply(lambda row: st.session_state.search_query in json.dumps(row.to_dict()).lower(), axis=1)].index)

# Get the indices of the JSON objects that meet the filter criteria
filtered_json_indices = [flattened_data[index]['json_index'] for index in filtered_indices]

# Display the list of JSONs as expandable items
st.write("Filtered JSON Objects:")
for index in filtered_json_indices:
    with st.expander(f"JSON {index + 1}"):
        st.json(json_objects[index])