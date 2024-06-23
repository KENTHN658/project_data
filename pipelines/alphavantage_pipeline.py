import pandas as pd

from etls.income_statement_etl import feth_income_statement, transform_income_statement, load_data_to_csv
from utils.constants import OUTPUT_PATH, API_KEY


def alphavantage_pipeline(file_name: str):
    # connecting to reddit instance
    instance = feth_income_statement(API_KEY, symbol="IBM")
    
    data = transform_income_statement(instance)
    data_df = pd.DataFrame(data)
    print(data_df)
    file_path = f'{OUTPUT_PATH}/{file_name}.csv'
    print("file path" + file_path)
    print("file" + file_name)
    load_data_to_csv(data_df, file_path)

    return file_path