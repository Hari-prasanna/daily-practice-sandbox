import pandas as pd
from pandas import json_normalize
import json

raw_events = [
    '{"event_type": "purchase", "user_id": "U1", "details": {"amount": 45.50, "currency": "USD"}}',
    '{"event_id": 102, "event_type": "view", "user_id": "U2", "details": {"item_id": "XYZ"}}',
    '{"event_id": 103, "event_type": "purchase", "user_id": "U1", "details": {"amount": -10.00, "currency": "USD"}}', 
    '{"event_id": 104, "event_type": "purchase", "user_id": "U3"}', 
    '{"event_id": 105, "event_type": "purchase", "user_id": "U4", "details": {"amount": 120.00, "currency": "EUR"}}',
    'BAD_DATA_SYSTEM_CRASH_ERROR_999'
]




# Convert valid JSON strings to dicts, skip the rest
valid_dicts = []
for e in raw_events:
    try:
        valid_dicts.append(json.loads(e))
    except:
        continue 

# Flatten everything at once
df_flat = pd.json_normalize(valid_dicts)
print(df_flat)