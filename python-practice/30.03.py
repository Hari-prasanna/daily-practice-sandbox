import requests
import pandas as pd
import os # Built-in Python library for interacting with your operating system
from dotenv import load_dotenv # The library we just installed

# --- 1. OPEN THE SAFE ---
# This line finds your .env file and loads the variables into memory
load_dotenv() 

# Grab the variables from the .env file
# If it can't find them, it will return what you put after the comma as a backup
url = os.getenv("API_ENDPOINT", "https://fakestoreapi.com/Users")
output_file = os.getenv("CSV_FILENAME", "backup_export.csv")

# --- 2. SETUP PANDAS ---
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# --- 3. EXTRACT THE DATA ---
response = requests.get(url)

if response.status_code == 200:
    raw_data = response.json()
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    raw_data = [] # Prevents the script from crashing if the API is down

# --- 4. THE CHEF (TRANSFORM) ---
def chef(raw_string):
    recipe = raw_string
    address = recipe.get("address", {})
    name = recipe.get("name", {})
    geo = address.get("geolocation", {})

    clean_url = {
        "id" : recipe.get("id"),
        "firstname" : name.get("firstname", "").title(),
        "lastname" : name.get("lastname", "").title(),
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

# --- 5. PROCESS THE ORDERS ---
clean_data = []

for user in raw_data:
    clean_user = chef(user)
    clean_data.append(clean_user)

df_clean = pd.DataFrame(clean_data)
print("Data successfully cleaned! Here is a preview:")
print(df_clean.head())

# --- 6. BOX IT UP (LOAD) ---
# We use the filename we grabbed from the .env file!
df_clean.to_csv(output_file, index=False)
print(f"\nSuccess! Your data has been saved to {output_file}")