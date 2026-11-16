import pandas as pd
import numpy as np
from datetime import datetime
import requests
import logging
import json
import os
import sqlalchemy as sqal
from typing import List, Dict, Any
from etl_store.exceptions import APIConnectionError, DataTransformationError
from etl_store.config import STORE_API_URL, DB_CONNECTION_STRING
from etl_store.utils import log_step, database_connection

logger = logging.getLogger("ProjectAlpha")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler = logging.FileHandler('logger.log')
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)


def exchange_to_pln(data_frame : pd.DataFrame) -> pd.DataFrame:
    try:
        data_frame["cena_pln"] = data_frame["cena_usd"] * 4.0
        return data_frame
    except KeyError as e:
        raise DataTransformationError(f"Missing column to count value: {e}")   

class ETL_Process:
    def __init__(self) -> None:
        self.store_api: str = STORE_API_URL

    @log_step("Downloading API data...")
    def extract_and_save(self) -> str:
        try:
            response = requests.get(self.store_api)
            response.raise_for_status()
            data = response.json()
            os.makedirs(os.path.dirname('/tmp/raw_data.json'), exist_ok=True)
            with open('/tmp/raw_data.json', 'w') as f:
                json.dump(data, f)
            return '/tmp/raw_data.json'
        except requests.exceptions.RequestException as e:
            logger.error(f"Data Import Failed : {e}")
            raise APIConnectionError(f"Error with API: {e}")


    @log_step("Framing Data by Pandas...")
    def transform_and_save_parquet(self, input_filepath: str) -> str:
        try:
            data_frame = pd.read_json(input_filepath)
            data_frame = data_frame.rename(columns = {
                "title":"tytul",
                "price" : "cena_usd",
                "category" : "kategoria",
            })
            data_frame = exchange_to_pln(data_frame)
            
            if "kategoria" not in data_frame.columns:
                raise DataTransformationError(f"Error with column \"kategoria\"")
            
            data_frame = data_frame[data_frame["kategoria"] != "electronics"]
            data_frame['rating'] = data_frame['rating'].astype(str)
            
            data = datetime.now()
            data_frame['rok'] = data.year
            data_frame['miesiac'] = data.month
            data_frame['dzien'] = data.day
            
            os.makedirs('/tmp/silver_layer/', exist_ok=True)
            data_frame.to_parquet(
                '/tmp/silver_layer/',
                engine = 'pyarrow',
                partition_cols = ['rok', 'miesiac', 'dzien'],
                index = False
            )
            
            return '/tmp/silver_layer/'
        except Exception as e:
            logger.error(f"Error : {e}")
            raise

    @log_step("Creating engine and SQL Database in PostgreSQL")
    def load_to_postgres(self, input_filepath : str) -> None:
        try:
            data_frame = pd.read_parquet(input_filepath)
            with database_connection(DB_CONNECTION_STRING) as conn:
                data_frame.to_sql(name = 'produkty',
                                con = conn,
                                if_exists='replace',
                                index = False)
        except Exception as e:
            logger.critical(f"No connection with DB - error: {e}")
            raise

if __name__ == "__main__":
    etl = ETL_Process()
    raw_path = etl.extract_and_save()
    clean_path = etl.transform_and_save_parquet(raw_path)
    etl.load_to_postgres(clean_path)
    print("SUCCESS! DATA IS COMPLETELY GETTIN!")