import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
from google.cloud import bigquery
from google.oauth2 import service_account

def fetch_inflation_rates(url):
    """Fetch HTML content from the URL."""
    try:
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        return soup
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def search_table(soup):
    """Find and return the data table from the HTML content."""
    if soup:
        datatable = soup.find("table", {"class": "std100 hover sticky"})
        return datatable
    return None

def transform_inflation_rates(datatable):
    """Transform the data table into a DataFrame and clean the data."""
    if datatable:
        df = pd.read_html(str(datatable))[0]
        for i in df.columns:
            if df[i].dtype == 'object':
                df[i] = df[i].str.replace(',', '').str.replace('%', '').astype(float)
        return df
    return pd.DataFrame()

def save_data_to_csv(data: pd.DataFrame, path: str):
    """Save DataFrame to a CSV file."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data.to_csv(path, index=False)
        print(f"Data saved to {path}")
    except Exception as e:
        print(f"Error saving data: {e}")


