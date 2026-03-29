#Unpack: Parse the JSON safely.

#Filter Status: Only keep "completed" orders. Drop canceled ones.

#Data Validation: Extract price and qty. If either is missing, OR if price is less than or equal to 0, drop the record.

#Transform (Math): Create a new field called total_revenue which is price * qty.

#Output Format: Return a clean record that looks like: {"order_id": "A1", "total_revenue": 25.0}.

import json
import pandas as pd

raw_orders = [
    '{"order_id": "A1", "status": "completed", "cart": {"price": 12.50, "qty": 2}}',
    '{"order_id": "A2", "status": "canceled", "cart": {"price": 45.00, "qty": 1}}',
    '{"order_id": "A3", "status": "completed", "cart": {"price": 9.99}}', # Missing qty
    '{"order_id": "A4", "status": "completed", "cart": {"price": -5.00, "qty": 2}}', # Bad price
    '{"order_id": "A5", "status": "completed", "cart": {"price": 100.00, "qty": 1}}'
]


def chef(raw_strigs):
    try:
        recipe = json.loads(raw_strigs)
    except json.jSONdecodeError:
        return None
    
    cart = recipe.get("cart",{})

    if recipe.get("status") == "canceled":
        return None
    
    price = cart.get("price",0)
    price = float(price)
    if price <= 0:
        return None
    
    quantity = cart.get("qty",0)
    quantity = int(quantity)

    total_revenue = price * quantity

    clean_orders = {
        "order_id" : recipe.get("order_id"),
        "status": recipe.get("status"),
        "price" : price,
        "qty": quantity,
        "total_revenue" : total_revenue
    }
    return clean_orders

clean_data = []

for orders in raw_orders:
    dish = chef(orders)
    if dish is not None:
        clean_data.append(dish)

df = pd.DataFrame(clean_data)
print(df)