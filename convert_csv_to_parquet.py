import os
from utils_duckdb import DuckClient

from config import file_path_rent_csv, file_path_sell_csv, file_path_rent_parquet, file_path_sell_parquet

def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"File {file_name} removed")
    else:
        print("The file does not exist")

duckCon = DuckClient(db_name="/Users/luigibungaro/personal/dubai-house-sell-rent-prices/dubai_housing.duckdb").get_client()

# OLD METHOD
# def build_path_csv(file_name):
#     bacis_path = "/".join(file_name.split("/")[:-1])
#     original_file_name = file_name.split("/")[-1]
#     new_file_name = original_file_name.split(".")[0] + ".parquet"
#     return f"{bacis_path}/{new_file_name}"

# def convert_cvs_to_parquet(file_name):
#     parquet_file = build_path_csv(file_name)
#     df = pd.read_csv(file_name)
#     df.to_parquet(parquet_file)
#     remove_file(file_name)
#     print(f"File {parquet_file} created")

if __name__ == "__main__":
    duckCon.execute(f"DROP TABLE IF EXISTS rent_contracts;")
    duckCon.execute(f"CREATE TABLE rent_contracts AS SELECT * FROM read_csv_auto('{file_path_rent_csv}', sample_size = -1);")
    duckCon.execute(f"COPY (select * from rent_contracts) to '{file_path_rent_parquet}';")

    duckCon.execute(f"DROP TABLE IF EXISTS sale_contracts;")
    duckCon.execute(f"CREATE TABLE sale_contracts AS SELECT * FROM read_csv_auto('{file_path_sell_csv}', sample_size = -1);")
    duckCon.execute(f"COPY (select * from sale_contracts) to '{file_path_sell_parquet}';")

    # remove_file(file_path_rent_csv)
    # remove_file(file_path_sell_csv)
    # convert_cvs_to_parquet(file_path_rent)
    # convert_cvs_to_parquet(file_path_sell)