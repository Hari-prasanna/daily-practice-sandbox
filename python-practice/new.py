import pandas as pd

raw_customers = [
    {"id": 1, "name": "   aLiCe smIth  ", "age": 28, "is_active": True},
    {"id": 2, "name": "bOb jOnEs", "age": None, "is_active": False},
    {"id": 3, "name": "charlie brown", "age": 17, "is_active": True},
    {"id": 4, "name": "  DaViD WIlliams", "age": 35}, 
    {"id": 5, "name": "EVE daviS", "age": 42, "is_active": True}
]



try:
    def chef(recepie):
        messy_name = recepie["name"]

        clean_name = messy_name.strip().title()


        clean_url = {
            "id" : recepie["id"],
            "name" : clean_name,
            "age" : recepie["age"],
            "is_active" : recepie.get("is_active",False)
        }

        return clean_url

    clean_customers = []


    for customers in raw_customers:
        if customers["age"] is None or customers["age"] < 18:
            continue
        cooked_customers = chef(customers)
        clean_customers.append(cooked_customers)

    df = pd.DataFrame(clean_customers)

    print(df)

except Exception as e:
    print(f"error: {e}")