import pandas as pd
from sqlalchemy import create_engine
pd.set_option('display.max_columns', None) 
try:
    data = pd.read_csv(r"C:\Users\hravichandra\Downloads\Bestandsabgleich.csv",sep=';')

    print(data.head())
except Exception as e:
    print(f"Error: {e}")
