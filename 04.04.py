import pandas as pd
import json
import logging
from dotenv import load_dotenv
import os
import boto3
from gspread import service_account
from gspread_dataframe import set_with_dataframe

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


load_dotenv()

raw_transactions = [
    '{"tx_id": "TX-901", "details": {"amount": 7500, "currency": "USD"}, "origin": "  USA  ", "type": "WIRE"}',
    '{"tx_id": "TX-902", "details": {"amount": 50, "currency": "USD"}, "origin": "uk", "type": "CARD"}',
    '{"tx_id": "TX-903", "details": {"amount": 12000, "currency": "EUR"}, "origin": "Cayman Islands", "type": "WIRE"}',
    'ERROR_SYSTEM_BUSY_RETRY_IN_5S',
    '{"tx_id": "TX-905", "details": {"amount": 0, "currency": "USD"}, "origin": "USA", "type": "CARD"}',
    '{"tx_id": "TX-906", "details": {"amount": 400, "currency": "USD"}, "origin": "  GERMANY ", "type": "Wire"}'
]

logging.info("initiatig the script :) ")

def chef(string):
    try:
        try:
            recipe = json.loads(string)
        except json.JSONDecodeError:
            logging.warning(f"Skipping corrupted string: {string} :(")
            return None
    
        details = recipe.get("details", {})

        amount = details.get("amount",0)
        origin = recipe.get("origin").strip().lower()

        if amount > 10000 or origin == 'cayman islands':
            risk_level = 'CRITICAL'
        elif amount > 5000:
            risk_level = 'HIGH'
        else:
            risk_level = 'LOW'

            
        raw_transactions_clean = {
            "tx_id" : recipe.get("tx_id"),
            "amount" : amount,
            "currency" : details.get("currency"),
            "origin" : origin,
            "type" : recipe.get("type").lower(),
            "risk_level" : risk_level
        }
        return raw_transactions_clean
        
    except Exception as e:
        logging.error(f"Error in block 1 cleaning: {e} ")



def download_to_local(clean_url,path):

    clean_string = []

    for dish in clean_url:
        cooked = chef(dish)
        if cooked is not None:
            clean_string.append(cooked)

    df = pd.DataFrame(clean_string)
    df.to_csv(path, index=False)
    return df


def upload_to_s3(local_path, bucket_name, s3_key):

    s3_client = boto3.client('s3')

    s3_client.upload_file(
        Filename = local_path,
        Bucket = bucket_name,
        Key = s3_key
    )
    return True

def upload_to_google_sheet(df, sheet_id, sheet_name, cred_path):
    logging.info("starting to filter")
    try:
        df_filter = df[df["risk_level"].isin(['HIGH','CRITICAL'])]

        gc = service_account(filename=cred_path)

        spreadsheet = gc.open_by_key(sheet_id)

        worksheet = spreadsheet.worksheet(sheet_name)

        worksheet.clear()

        set_with_dataframe(worksheet,df_filter)
        return True
    except Exception as e:
        logging.error(f"Error in google_sheet upload: {e}")

if __name__ == "__main__":

    bucket_name = os.getenv("AWS_S3_BUCKET")
    s3_key = f"banking-lakehouse/raw/sample.csv"
    path = "test/sample.csv"
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    sheet_name = os.getenv("GOOGLE_SHEET_NAME")
    cred_path = os.getenv("GOOGLE_CREDENTIALS_PATH")


    download = download_to_local(raw_transactions, path)
    logging.info("download_successful")
    s3_upload = upload_to_s3(path, bucket_name, s3_key)
    logging.info("successful_uploaded")
    google_upload = upload_to_google_sheet(download,sheet_id, sheet_name, cred_path)
    logging.info("successful_uploaded_googlesheet")

