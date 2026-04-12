import logging
import os
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from sqlalchemy import create_engine, text
import io
import boto3
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Opening secure space for credentials from os")
load_dotenv()

def db_connection():
    try:
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")

        url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        engine = create_engine(url)

        with engine.connect() as connection: #with as context manager: it opens the alias connection, execute and closes immediatly after execution without writing end extra line
            query = text('SELECT count(*) FROM "dpt-hp".stg_movies')
            result = connection.execute(query)
            count = result.scalar() #takes the first row of the table in this case count displays as one row
            logging.info(f"Connection successful! Row count: {count}")
        return engine
    except Exception as e:
        logging.error(f"Error with connection: {e}")
        return None


def s3_upload(df, bucket_name, key):

    try:
        csv_buffer = io.StringIO() #creates a virtual container in the RAM

        df.to_csv(csv_buffer, index=False) #pushing the data to the container

        s3_resource = boto3.resource('s3') 

        s3_resource.Object(bucket_name,key).put(Body=csv_buffer.getvalue()) #adding the content to the bucket by taking the content from the container

        return True
    except Exception as e:
        logging.error(f"error in upload to s3 block: {e}")
        return None

def gs_upload(df, sheet_name, sheet_id, cred_path):

    try:
        gc = gspread.service_account(filename=cred_path) #assigning key

        spreadsheet = gc.open_by_key(sheet_id) #using key to open sheet

        worksheet = spreadsheet.worksheet(sheet_name) #then sheet_name

        worksheet.clear() #clearning the sheet

        set_with_dataframe(worksheet, df) #inserting values in the sheet

        return True
    except Exception as e:
        logging.error(f"error in gs connection block: {e}")
        return None

if __name__ == "__main__":

#config
    cred_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    sheet_name = os.getenv("GOOGLE_SHEET_NAME")
    bucket_name = os.getenv("AWS_S3_BUCKET")
    s3_key = f"banking-lakehouse/test/TMDB_test.csv"


#excute
    try:
        connected_engine = db_connection()

        if connected_engine:
            query = text('SELECT * FROM "dpt-hp".stg_movies')
            df = pd.read_sql(query, connected_engine)
            logging.info(f"Data extracted. Shape: {df.shape}") #shape of the data
        else:
            logging.error(f"error in main block: {connected_engine}")

        if df is not None:
            s3_delivery_success = s3_upload(df, bucket_name, s3_key)
            logging.info(f"successfully delivered to S3 path: {s3_key}")
            
            if s3_delivery_success:
                gs_delivery = gs_upload(df, sheet_name, sheet_id, cred_path)
                logging.info(f"successfully delivered to google sheet: {sheet_name}")
            else:
                logging.error(f"S3_upload failed so skipping google_sheet_upload")
        else:
            logging.error(f"error in main block: {df}")

    except Exception as e:
        logging.error(f"Critical error in main pipeline: {e}")


    
    