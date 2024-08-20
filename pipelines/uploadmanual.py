import datetime
import os
import pandas as pd
from utils.constants import ACCESS_KEY, OUTPUT_PATH

def write_kaggle_data():
    file_name = f'inflation_rates_{ datetime.now().year}.csv'
    files = os.listdir(OUTPUT_PATH)
    print(f"Files in output path: {file_name}")

    for f in files:
        if f != file_name:
            file_path = os.path.join(OUTPUT_PATH, f)
            df = pd.read_csv(file_path)
            try:
                df.to_csv(f'abfs://dataeng@projectdataeng.dfs.core.windows.net/data/{f}',
                          storage_options={
                              'account_name': 'projectdataeng',
                              'account_key': f'{ACCESS_KEY}'
                          }, index=False)
                print(f"Data uploaded to Azure Blob Storage: {f}")
            except Exception as e:
                print(f"Error saving data on cloud: {e}")
