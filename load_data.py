import requests
import json
import pandas as pd

url = "https://jsonplaceholder.typicode.com/users"

pd.set_option('display.max_columns', None)  # Shows all columns
pd.set_option('display.width', 1000)


def worker(recipie):

    clean_name = recipie["name"].strip().lower().title()
    clean_email = recipie["email"].strip().lower()
    clean_phone_number = recipie["phone"].replace('-',' ')


    clean_string = {
        "id" : recipie["id"],
        "name" : clean_name,
        "username" : recipie["username"],
        "email" : clean_email,
        "street" : recipie["address"]["street"],
        "suite" : recipie["address"]["suite"],
        "city" : recipie["address"]["city"],
        "zipcode" : recipie["address"]["zipcode"],
        "phone" : clean_phone_number,
        "website" : recipie["website"],
        "company" : recipie["company"]  
  
            }
    return clean_string


clean_data = []



try:
    responce = requests.get(url)

    raw_data = responce.json()

    for test in raw_data:
        cleaned = worker(test)
        clean_data.append(cleaned)

    df = pd.DataFrame(clean_data)
    
    print(df.keys())
    print(df.head())

except Exception as e:
    print(f"Error: {e}")