import json
import os
import pandas as pd
from datetime import datetime
from utils.constants import OUTPUT_PATH

def get_data_page(url):
    import requests

    print("Getting data page...", url)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # check if the request is successful

        return response.text
    except requests.RequestException as e:
        print(f"An error occured: {e}")


def get_data_data(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", {"class": "std100 hover sticky"})
    return table


def extract_data_from_website(**kwargs):
    url = kwargs['url']
    html = get_data_page(url)
    table_html  = get_data_data(html)

    data = []

    headers = [header.text for header in table_html.find_all('th')]
    for row in table_html.find_all('tr')[1:]:  # Skip the header row
        values = [value.text for value in row.find_all('td')]
        row_dict = {headers[i]: values[i] for i in range(len(headers))}
        data.append(row_dict)

    json_rows = json.dumps(data)
    kwargs['ti'].xcom_push(key='rows', value=json_rows)
    # print(json_rows)

    return 0

def transform_website_data(**kwargs):
    data = kwargs['ti'].xcom_pull(key='rows', task_ids='extract_data_from_website')
    data = json.loads(data)
    inflation_df = pd.DataFrame(data)

    
    for i in inflation_df.columns:
        if inflation_df[i].dtype == 'object' and i != "Year" :
            inflation_df[i] = inflation_df[i].str.replace(',', '')  # ลบเครื่องหมายคั่นหลักพัน
            inflation_df[i] = inflation_df[i].str.replace('%', '')  # ลบเครื่องหมาย %
            inflation_df[i] = inflation_df[i].astype(float)         # แปลงเป็น float
        else:
            continue
    
    
    # push to xcom
    kwargs['ti'].xcom_push(key='rows', value=inflation_df.to_json())

    print(inflation_df)

def write_website_data(**kwargs):
    
    data = kwargs['ti'].xcom_pull(key='rows', task_ids='transform_website_data')

    data = json.loads(data)
    data = pd.DataFrame(data)

    file_name = f'inflation_rates_{ datetime.now().year}'
    file_path = f'{OUTPUT_PATH}/{file_name}.csv'
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        data.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error saving data: {e}")


