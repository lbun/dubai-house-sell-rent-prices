from utils_duckdb import DuckClient
from config import file_path_rent_parquet, file_path_sell_parquet, duckdb_path

# /Users/luigibungaro/personal/dubai-house-sell-rent-prices/dubai_housing.duckdb
duckCon = DuckClient(db_name=duckdb_path).get_client()

duckCon.execute(f"CREATE TABLE rent_contracts AS SELECT * FROM read_parquet('{file_path_rent_parquet}');")
duckCon.execute(f"CREATE TABLE sale_contracts AS SELECT * FROM read_parquet('{file_path_sell_parquet}');")



