import os
import requests
import pandas as pd
import boto3
from io import BytesIO
from dotenv import load_dotenv

# 1. Swipe the ID Badge to load the .env passwords into memory
load_dotenv()

# ==========================================
# THE CHEF: Extract and Clean the Data
# ==========================================
def fetch_and_clean_api_data(url):
    print("👨‍🍳 Chef: Fetching data from API...")
    response = requests.get(url)
    raw_data = response.json()
    
    clean_data = []
    
    for recipe in raw_data:
        clean_string = {
            "id": recipe["id"],
            "name": recipe["name"].strip().lower().title(),
            "username": recipe["username"],
            "email": recipe["email"].strip().lower(),
            "city": recipe["address"]["city"],
            "phone": recipe["phone"].replace('-', ' '),
            "company_name": recipe["company"]["name"]
        }
        clean_data.append(clean_string)

    df = pd.DataFrame(clean_data)
    print("👨‍🍳 Chef: Data cleaned and packed into DataFrame.")
    return df

# ==========================================
# THE DRIVER: Upload to AWS S3
# ==========================================
def upload_dataframe_to_s3(df, s3_key):
    print("🚚 Driver: Vacuum sealing data into Parquet...")
    
    # 1. Connect to AWS
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    bucket_name = os.getenv('AWS_S3_BUCKET')
    
    # 2. Create the floating RAM container
    parquet_buffer = BytesIO()
    df.to_parquet(parquet_buffer, engine='pyarrow', index=False)
    
    # 3. Deliver the package
    print(f"🚚 Driver: Driving to s3://{bucket_name}/{s3_key}")
    s3_client.put_object(
        Bucket=bucket_name,
        Key=s3_key,
        Body=parquet_buffer.getvalue()
    )
    print("✅ Delivery Complete!")

# ==========================================
# THE MANAGER'S DESK: Run the Pipeline
# ==========================================
if __name__ == "__main__":
    try:
        api_url = "https://jsonplaceholder.typicode.com/users"
        target_s3_path = "sandbox/test/users_api_data.parquet"
        
        # 1. Tell the Chef to make the food
        final_dataframe = fetch_and_clean_api_data(api_url)
        
        # 2. Hand the food to the Driver
        upload_dataframe_to_s3(final_dataframe, target_s3_path)
        
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")