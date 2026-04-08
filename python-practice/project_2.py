#Handle Corruption: Catch the corrupt string safely without crashing the script.

#Filter Traffic: Drop any record where the type is "bot". We only want human traffic.

#Clean the Page URL: Strip the leading/trailing spaces from the page string and make it entirely lowercase.

#Handle Missing Data: If the country is missing (like in the third record), safely default it to "unknown".

#Output Format: Return a clean record: {"ip": "192.168.1.1", "page": "/home", "country": "USA"} (Notice we drop the type column in the final output since we know they are all humans).


import json 
import pandas as pd

raw_logs = [
    '{"ip": "192.168.1.1", "type": "human", "page": "   /HOME   ", "country": "USA"}',
    '{"ip": "10.0.0.5", "type": "bot", "page": "/pricing", "country": "UK"}',
    '{"ip": "172.16.0.8", "type": "human", "page": "/checkout"}', # Missing country
    'FATAL_SERVER_ERROR_UNABLE_TO_WRITE_LOG', # Corrupt string!
    '{"ip": "192.168.1.9", "type": "human", "page": "  /contact  ", "country": "CAN"}'
]

def chef(raw_string):
    try:
        recipe = json.loads(raw_string)
    except json.JSONDecodeError:
        return None
    
    if recipe.get("type") == "bot":
        return None
    
    messy_page = recipe.get("page")
    messy_page = str(messy_page)
    clean_page = messy_page.strip().replace("/","").lower()

    clean_logs = {
        "ip" : recipe.get("ip"),
        "type" : recipe.get("type"),
        "page" : clean_page,
        "country" : recipe.get("country","Unknown")
    }
    return clean_logs

cleaned_logs = []

for logs in raw_logs:
    cooked = chef(logs)
    if cooked is not None:
        cleaned_logs.append(cooked)


df = pd.DataFrame(cleaned_logs)

print(df)