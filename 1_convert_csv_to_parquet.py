"""
It takes in inout the downloaded csv files and:
- creates table in duckdb database
- converts them to parquet format
"""

import os
from utils_duckdb import DuckClient

from config import file_path_rent_csv, file_path_sell_csv, file_path_rent_parquet, file_path_sell_parquet

def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"File {file_name} removed")
    else:
        print("The file does not exist")
        
path_db = "/Users/luigibungaro/Library/CloudStorage/OneDrive-GulfAgencyCompany/files_macbook/data/duck_databases/dubai-house-market.db"
duckCon = DuckClient(db_name=path_db).get_client()


if __name__ == "__main__":
    duckCon.execute(f"DROP TABLE IF EXISTS rent_contracts;")
    duckCon.execute(f"CREATE TABLE rent_contracts AS SELECT * FROM read_csv_auto('{file_path_rent_csv}', sample_size = -1);")
    duckCon.execute(f"COPY (select * from rent_contracts) to '{file_path_rent_parquet}';")

    duckCon.execute(f"DROP TABLE IF EXISTS sale_contracts;")
    duckCon.execute(f"CREATE TABLE sale_contracts AS SELECT * FROM read_csv_auto('{file_path_sell_csv}', sample_size = -1);")
    duckCon.execute(f"COPY (select * from sale_contracts) to '{file_path_sell_parquet}';")

