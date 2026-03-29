import pandas as pd

raw_emails = [" JOHN@gmail.com ", "alice@YAHOO.com", "  BOB@hotmail.com"]

def chef(recepie):
    dish = recepie.strip().lower()
    return dish

clean_email = []


for test in raw_emails:
    clean_test = chef(test)
    clean_email.append(clean_test)

df = pd.DataFrame(clean_email)

print(df)


messy_products = ["   iPHone 14   ", "macbook PRO", "  AirPods   ", " ipad mini  "]


def chef(recepie):
    dish = recepie.strip().upper().replace(" ","_")
    return dish

clean_products = []

for products in messy_products:
    cooked_products = chef(products)
    clean_products.append(cooked_products)
df = pd.DataFrame(clean_products)

print(df)