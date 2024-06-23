import pandas as pd
from etls.INCOME_STATEMENT_ETL import fetch_income_statement, transform_income_statement, load_data_to_csv
from utils.constants import OUTPUT_PATH, API_KEY

def income_pipeline(file_name: str):
    instance = fetch_income_statement(API_KEY, symbol="IBM")
    data = transform_income_statement(instance)
    data_df = pd.DataFrame(data)
    file_path = f'{OUTPUT_PATH}/{file_name}.csv'
    load_data_to_csv(data_df, file_path)
    return file_path
