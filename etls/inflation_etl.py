import sys
import requests
import os
import numpy as np
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
import requests

def feth_inflation_rates(url):
    resource =  url
    res = requests.get(resource)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def search_table(soup):
    datatable = soup.find("table", {"class": "std100 hover sticky"})
    return datatable

def transform_inflation_rates(datatable):
    df = pd.read_html(str(datatable))
    df = pd.DataFrame(df[0])
    for i in df.columns:
        if df[i].dtype == 'object':
            df[i] = df[i].str.replace(',', '')  # ลบเครื่องหมายคั่นหลักพัน
            df[i] = df[i].str.replace('%', '')  # ลบเครื่องหมาย %
            df[i] = df[i].astype(float)         # แปลงเป็น float
        else:
            continue

    return df



def save_data_to_csv(data: pd.DataFrame, path: str):
    print("load csv 123")
    statetus = os.makedirs(os.path.dirname(path), exist_ok=True)
    print(statetus)
    data.to_csv(path, index=False)



