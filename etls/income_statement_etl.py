import sys
import numpy as np
import pandas as pd
import requests
import os


def feth_income_statement(apikey, symbol):
    print(apikey)
    print(symbol)
    url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo'
    r = requests.get(url)
    data = r.json()
    print("HELLO KEN")
    return data

def transform_income_statement(data):
    annual_reports = data.get("annualReports", [])
    df = pd.DataFrame(annual_reports)
    df['fiscalDateEnding'] = pd.to_datetime(df['fiscalDateEnding'])
    df = df.apply(pd.to_numeric, errors='ignore')
    return df

def load_data_to_csv(data: pd.DataFrame, path: str):
    print("load csv 123")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data.to_csv(path, index=False)
