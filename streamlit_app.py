import streamlit as st
import json
import pandas as pd

# Example list of JSON objects. Replace this with your actual JSON objects or the method to load/fetch them.
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

# Convert JSON objects to strings for display (if needed)
json_strings = [json.dumps(obj, indent=2) for obj in json_objects]

# Preprocess JSON objects to create a flat structure for pandas
flattened_data = []
for obj in json_objects:
    # Check if 'trigger' is a dictionary and access 'type' accordingly
    trigger_type = obj["trigger"]["type"] if isinstance(obj["trigger"], dict) else None
    for component in obj["components"]:
        flattened_data.append({
            "component_definition": component["definition"],
            "component_category": component["category"],
            "trigger_type": trigger_type,
        })

# Convert the preprocessed data to a DataFrame
df = pd.DataFrame(flattened_data)

# Initialize filters in Streamlit's session state if they're not already set
if 'filters' not in st.session_state:
    st.session_state.filters = {"component_definition": [], "component_category": [], "trigger_type": []}

# Sidebar for filtering
st.header("Filter options")
filter_key = st.selectbox("Filter by", options=["component_definition", "component_category", "trigger_type"], key="filter_by_key")

# Generate a list of unique values for the selected filter key
unique_values = df[filter_key].unique().tolist()
unique_values.sort()  # Sort the list for easier browsing

# Multiselect for the filter values, using the filter_key to save and load selected values
selected_filters = st.multiselect(f"Select {filter_key}", unique_values, default=st.session_state.filters[filter_key], key=f"select_{filter_key}")

# Save the selected filters back to the session state
st.session_state.filters[filter_key] = selected_filters

# Display all selected filters/tags
st.write("Selected filters:")
for key, values in st.session_state.filters.items():
    if values:
        st.write(f"{key.capitalize().replace('_', ' ')}: {', '.join(map(str, values))}")

# Apply filters to the DataFrame
filtered_df = df
for key, values in st.session_state.filters.items():
    if values:
        filtered_df = filtered_df[filtered_df[key].isin(values)]

# Display filtered DataFrame
if not filtered_df.empty:
    st.dataframe(filtered_df)
else:
    st.write("No entries match your filter criteria.")