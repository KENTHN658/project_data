import pandas as pd

from etls.inflation_etl import feth_inflation_rates, save_data_to_csv, search_table, transform_inflation_rates 
from utils.constants import OUTPUT_PATH


def inflation_pipeline(file_name: str, url):
    text_html = feth_inflation_rates(url)
    soup = search_table(text_html)
    transform_data = transform_inflation_rates(soup)
    file_path = f'{OUTPUT_PATH}/{file_name}.csv'
    save_data = save_data_to_csv(transform_data,file_path)
    print("file path" + file_path)
    print("file name" + file_name)

    return file_path