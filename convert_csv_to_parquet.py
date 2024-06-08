import pandas as pd
import os

file_path_rent = "/Users/luigibungaro/personal/dubai-house-sell-rent-prices/data/Rent_Contracts.csv"
file_path_sell = "/Users/luigibungaro/personal/dubai-house-sell-rent-prices/data/Transactions.csv"

def build_path_csv(file_name):
    bacis_path = "/".join(file_name.split("/")[:-1])
    original_file_name = file_name.split("/")[-1]
    new_file_name = original_file_name.split(".")[0] + ".parquet"
    return f"{bacis_path}/{new_file_name}"

def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"File {file_name} removed")
    else:
        print("The file does not exist")

def convert_cvs_to_parquet(file_name):
    parquet_file = build_path_csv(file_name)
    df = pd.read_csv(file_name)
    df.to_parquet(parquet_file)
    remove_file(file_name)
    print(f"File {parquet_file} created")

if __name__ == "__main__":
    convert_cvs_to_parquet(file_path_rent)
    convert_cvs_to_parquet(file_path_sell)