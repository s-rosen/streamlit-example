import json
import pandas as pd

data_path = "/mnt/fd_ai_t2af_data/datasets/synthetic/synthetic_flows_2024-03-02_annot/train/data.jsonl"
data = []

with open(data_path, 'r') as file:
    for line in file:
        data.append(json.loads(line))
        print(line)

df = pd.DataFrame(data)

print(df)