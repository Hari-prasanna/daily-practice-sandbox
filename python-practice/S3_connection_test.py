import os
import boto3
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv

# 1. Load the VIP Keycard from your .env file
load_dotenv()

def run_sandbox_test():
    print("🚀 Starting S3 Sandbox Test...")
    
    # 2. Create some fake sample data
    data = {
        'movie_id': [1, 2, 3],
        'title': ['The Cloud Architect', 'Revenge of the S3', 'Return of the Databricks'],
        'revenue': [1000000, 2500000, 5000000]
    }
    df = pd.DataFrame(data)
    print("✅ Created sample Pandas DataFrame.")
    
    # 3. Connect to AWS S3
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )
    bucket_name = os.getenv('AWS_S3_BUCKET')
    s3_key = 'sandbox/test/sample.parquet'
    
    # 4. Convert to Parquet in-memory
    parquet_buffer = BytesIO()
    df.to_parquet(parquet_buffer, engine='pyarrow', index=False)
    
    # 5. Upload to S3
    print(f"📦 Uploading to s3://{bucket_name}/{s3_key}...")
    s3_client.put_object(
        Bucket=bucket_name,
        Key=s3_key,
        Body=parquet_buffer.getvalue()
    )
    
    print("🎉 SUCCESS! The file is now in the cloud.")

if __name__ == "__main__":
    run_sandbox_test()