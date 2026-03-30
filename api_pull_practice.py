import requests
import pandas as pd
import os
from dotenv import load_dotenv
import gspread
from gspread_dataframe import set_with_dataframe

load_dotenv()

url = os.getenv("url")
sheet_name = os.getenv("sheet_name")
sheet_id = os.getenv("sheet_id")
google_cred_path = os.getenv("google_cred_path")


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

url = "https://fakestoreapi.com/Users"

response = requests.get(url)

if response.status_code == 200:
    raw_data = response.json()
else:
    print("Failed to fetch data. Status code:", response.status_code)

def chef(raw_string):
    recipe = raw_string
    address = recipe.get("address",{})
    name = recipe.get("name",{})
    geo =address.get("geolocation",{})

    clean_url = {
    "id" : recipe.get("id"),
    "firstname" : name.get("firstname").title(),
    "lastname" : name.get("lastname").title(),
    "email" : recipe.get("email"),
    "username" : recipe.get("username"),
    "password" : recipe.get("password"),
    "phone" : recipe.get("phone"),
    "city" : address.get("city"),
    "street" : address.get("street"),
    "house_number" : address.get("number"),
    "zipcode" : address.get("zipcode"),
    "latitude" : geo.get("lat"),
    "longitude" : geo.get("long")
    }
    return clean_url

clean_data = []

for user in raw_data:
    clean_user = chef(user)
    clean_data.append(clean_user)

df_clean = pd.DataFrame(clean_data)

try:
    gc = gspread.service_account(filename=google_cred_path)

    spreadsheet = gc.open_by_key(sheet_id)

    worksheet = spreadsheet.worksheet(sheet_name)

    worksheet.clear()

    set_with_dataframe(worksheet, df_clean)
except Exception as e:
    print("An error occurred while uploading to Google Sheets:", e)