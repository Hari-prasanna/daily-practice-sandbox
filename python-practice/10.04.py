import pandas as pd
import logging
from dotenv import load_dotenv
import gspread
from gspread_dataframe import set_with_dataframe
import json
import os

load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format= '%(asctime)s - %(levelname)s - %(message)s'
)


raw_sales = [
    '{"sale_id": "S1", "item": "Laptop", "price": 1000, "timestamp": "2023-10-01 10:00"}',
    '{"sale_id": "S2", "item": "Mouse", "price": 25, "timestamp": "2023-10-01 10:05"}',
    '{"sale_id": "S1", "item": "Laptop", "price": 1000, "timestamp": "2023-10-01 10:00"}', # DUPLICATE!
    '{"sale_id": "S3", "item": "Monitor", "price": -200, "timestamp": "2023-10-01 10:10"}', # BAD DATA
    '{"sale_id": "S4", "item": "Keyboard", "price": 50, "timestamp": "2023-10-01 10:15"}'
]


logging.info("started cleaning the raw string")

def chef(string):
    try:
        try:
            recipe = json.loads(string)
        except json.JSONDecodeError:
            logging.warning(f"we have a bad data inside: {string}")
            return None
    
        price = recipe.get("price")

    
        if price < 0:
            logging.warning(f"eliminatinating negative values in price column from the row: {recipe.get("sale_id")}")
            return None
    

        raw_clean_string = {
            "sale_id" : recipe.get("sale_id"),
            "item" : recipe.get("item"),
            "price" : price,
            "timestamp" : recipe.get("timestamp")
        
        }
        return raw_clean_string
    except Exception as e:
        logging.error(f"Error in chef block:{e}")

def creating_data_frame(raw_string):
    try:
        clean_data = []

        for dish in raw_string:
            cooked = chef(dish) # connecting the chef in this block

            if cooked is not None:
                clean_data.append(cooked)

        df = pd.DataFrame(clean_data)
        df = df.drop_duplicates(subset=['sale_id'])
        return df
    except Exception as e:
        logging.error(f"error in creating dataframe {e}")

def to_sheets(data, sheet_id, sheet_name, cred_path):

    try:

        gc = gspread.service_account(filename=cred_path) #handing over the key

        spreadsheet = gc.open_by_key(sheet_id) # opening the googlesheet with key

        worksheet = spreadsheet.worksheet(sheet_name) #opening the sheet

        worksheet.clear() #clearing it before sending the data

        set_with_dataframe(worksheet, data)

        return True
    except Exception as e:
        logging.error(f"Error in sending to sheet block: {e}")



#final block

if __name__ == "__main__":

#config
    cred_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    sheet_name = os.getenv("GOOGLE_SHEET_NAME")


#loading
    cleaned_df = creating_data_frame(raw_sales)

    if not cleaned_df.empty:
        success = to_sheets(cleaned_df, sheet_id, sheet_name, cred_path)
        if success:
            logging.info(f"Success! Data moved to {sheet_name}. Rows: {len(cleaned_df)}")
    else:
        logging.warning("No data to upload.")