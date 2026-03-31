import pandas as pd
import json
import gspread
from gspread_dataframe import set_with_dataframe
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()

google_cred_path = os.getenv("google_cred_path")
sheet_id = os.getenv("sheet_id")
sheet_name = os.getenv("sheet_name")

raw_fitness_data = [
    '{"user_id": 1, "activity": "   RUNning  ", "metrics": {"calories": 450, "duration_min": 30}, "status": "active"}',
    '{"user_id": 2, "activity": "Walking", "metrics": {"calories": 100, "duration_min": 60}, "status": "active"}',
    '{"user_id": 3, "activity": "Cycling", "metrics": {"calories": 600, "duration_min": 45}, "status": "active"}',
    '{"user_id": 4, "activity": "Running", "metrics": {"calories": -50, "duration_min": 10}, "status": "active"}', 
    'SYSTEM_NETWORK_TIMEOUT_RETRY_5', 
    '{"user_id": 6, "activity": "  cycLing ", "metrics": {"duration_min": 20}, "status": "active"}', 
    '{"user_id": 7, "activity": "Swimming", "metrics": {"calories": 500, "duration_min": 40}, "status": "inactive"}'
]


def chef(raw_string):
    try:
        recipe = json.loads(raw_string)
    except json.JSONDecodeError:
        logging.warning(f"Skipping corrupted string: {raw_string}")
        return None

    metrics = recipe.get("metrics", {})

    calories = metrics.get("calories")

    duration_min = metrics.get("duration_min")

    if calories is None or calories < 0:
        return None
    if duration_min < 0:
        return None

    burn_rate = round(calories/duration_min,2)

    clean_fitness_data = {
        "user_id" : recipe.get("user_id"),
        "activity": recipe.get("activity").strip().title(),
        "calories" : calories,
        "duration_min": duration_min,
        "status" : recipe.get("status"),
        "burn_rate" : burn_rate
    }
    return clean_fitness_data

logging.info("Starting Fitness Data Pipeline...")
clean_data = []

for dish in raw_fitness_data:
    cooked = chef(dish)
    if cooked is not None:
        clean_data.append(cooked)

df = pd.DataFrame(clean_data)
logging.info(f"Transformation complete. {len(df)} records ready for upload.")


try:
    gc = gspread.service_account(filename=google_cred_path)

    spreadsheet = gc.open_by_key(sheet_id)

    worksheet = spreadsheet.worksheet(sheet_name)

    worksheet.clear()

    set_with_dataframe(worksheet, df)

    logging.info("Successfully updated Google Sheet! 🎉")

except Exception as e:
    logging.error(f"Pipeline Failed! Error Details: {e}")
