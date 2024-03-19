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
for obj in json_objects:
    # Determine the trigger_type, accounting for the possible absence of the "trigger" key or it being a string
    trigger_type = obj["trigger"]["type"] if isinstance(obj.get("trigger", {}), dict) and "type" in obj["trigger"] else "None"
    for component in obj.get("components", []):
        flattened_data.append({
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
search_query = st.text_input("Search JSONs", value=st.session_state.search_query)
st.session_state.search_query = search_query

# Function to apply filters to the DataFrame
def apply_filters(df, search_query, filters):
    filtered_df = df
    for key, values in filters.items():
        if values:
            filtered_df = filtered_df[filtered_df[key].isin(values)]
    if search_query:
        filtered_df = filtered_df[df.apply(lambda row: search_query.lower() in json.dumps(row.to_dict()).lower(), axis=1)]
    return filtered_df

# Sidebar for filtering
st.sidebar.header("Filter options")
filter_key = st.sidebar.selectbox("Filter by", options=["component_definition", "component_category", "trigger_type"], key="filter_by_key")

# Generate a list of unique values for the selected filter key
unique_values = df[filter_key].unique().tolist()
unique_values.sort()  # Sort the list for easier browsing

# Multiselect for the filter values
selected_filters = st.sidebar.multiselect(f"Select {filter_key}", unique_values, default=st.session_state.filters[filter_key], key=f"select_{filter_key}")

# Update the session state for filters
st.session_state.filters[filter_key] = selected_filters

# Apply the filters and search query to the DataFrame
filtered_df = apply_filters(df, st.session_state.search_query, st.session_state.filters)

# Display the selected filters
st.write("Selected filters:")
for key, values in st.session_state.filters.items():
    if values:
        st.write(f"{key.capitalize().replace('_', ' ')}: {', '.join(map(str, values))}")

# Allow the user to select and view individual JSONs from the filtered results
if not filtered_df.empty:
    selected_index = st.selectbox("Select a JSON to view", range(len(filtered_df)), format_func=lambda x: f"JSON {x + 1}")
    selected_json = json_objects[selected_index]  # Assuming `filtered_df` is in the same order as `json_objects`
    st.json(selected_json)
else:
    st.write("No entries match your filter criteria.")