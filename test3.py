import json
import pandas as pd

raw_events = [
    '{"event_type": "purchase", "user_id": "U1", "details": {"amount": 45.50, "currency": "USD"}}',
    '{"event_id": 102, "event_type": "view", "user_id": "U2", "details": {"item_id": "XYZ"}}',
    '{"event_id": 103, "event_type": "purchase", "user_id": "U1", "details": {"amount": -10.00, "currency": "USD"}}', 
    '{"event_id": 104, "event_type": "purchase", "user_id": "U3"}', 
    '{"event_id": 105, "event_type": "purchase", "user_id": "U4", "details": {"amount": 120.00, "currency": "EUR"}}',
    'BAD_DATA_SYSTEM_CRASH_ERROR_999'
]



try:
    def chef(raw_string):

        try:
            recipe_dict = json.loads(raw_string)
        except json.JSONDecodeError:
            return None

        if recipe_dict.get("event_type") != "purchase":
            return None

        details = recipe_dict.get("details", {})

        if details.get("amount") is None or details.get("amount")  <= 0:
            return None

        return {
        "event_id" : recipe_dict.get("event_id"),
        "event_type" : recipe_dict.get("event_type"),
        "user_id" : recipe_dict.get("user_id"),
        "item_id" : details.get("item_id"),
        "amount" : details.get("amount"),
        "currency" : details.get("currency")
        }
    
    clean_events = []

    for events in raw_events:
        cooked_events = chef(events)
        if cooked_events is not None:
            clean_events.append(cooked_events)

    df = pd.DataFrame(clean_events)
    print(df)
except Exception as e:
    print(f"error: {e}")