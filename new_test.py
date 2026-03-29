import json
import pandas as pd

raw_sensor_data = [
    '{"sensor_id": "S-100", "status": "active", "location": "   RoofTop  ", "metrics": {"temp_c": 22.5, "humidity": 45}}',
    '{"sensor_id": "S-101", "status": "inactive", "location": "basement", "metrics": {"temp_c": 15.0, "humidity": 60}}',
    '{"sensor_id": "S-102", "status": "active", "metrics": {"temp_c": -5.0, "humidity": 55}}', 
    '{"sensor_id": "S-103", "status": "active", "location": "garden", "metrics": {"humidity": 50}}', 
    'SYSTEM_ERROR_CONNECTION_LOST_NODE_9',
    '{"sensor_id": "S-105", "status": "active", "location": "  bAlcony ", "metrics": {"temp_c": 30.0}}' 
]


def chef(raw_sensor_string):
    try:
        recipe = json.loads(raw_sensor_string)
    except json.JSONDecodeError:
        return None
    
    metrics = recipe.get("metrics",{})

    location_clean = recipe.get("location","Unknown")
    location_clean = str(location_clean).strip().title()

    temp_c = metrics.get("temp_c",0)
    if temp_c <= 0 or temp_c is None:
        return None
    temp_c = float(temp_c)
    temp_f = (temp_c * 9/5) + 32

    if recipe.get("status") != "active":
        return None

    clean_sensor_data = {
        "sensor_id" : recipe.get("sensor_id"),
        "status" : recipe.get("status"),
        "location" : location_clean,
        "temp_c" : metrics.get("temp_c"),
        "temp_f" : temp_f,
        "humidity" : metrics.get("humidity")
    }

    return clean_sensor_data

clean_data = []
try:
    for data in raw_sensor_data:
        clean_data_loop = chef(data)
        if clean_data_loop is not None:
            clean_data.append(clean_data_loop)

    df = pd.DataFrame(clean_data)

    print(df)
except Exception as e:
    print(f"error: {e}")