import sys
import pandas as pd

# STD COLUMNS NAMES -->
# day_dt
def convert_csv_to_parquet(csv_path):
    df = pd.read_csv(csv_path)
    parquet_path = csv_path.replace(".csv", ".parquet")
    df.to_parquet(parquet_path)

class SellTransactions:
    def __init__(self, df):
        self.df = df
        self.columns_of_interest = ["trans_group_en", "procedure_name_en", "instance_date", "property_type_en", "property_sub_type_en", "property_usage_en",
                      "reg_type_en", "area_name_en", "building_name_en", "project_name_en", "master_project_en", "nearest_landmark_en",
                      "nearest_metro_en", "nearest_mall_en", "rooms_en", "has_parking", "procedure_area", "actual_worth", "meter_sale_price"]
    
    def check_columns_in_df(self):

        if all(col in self.df.columns for col in self.columns_of_interest):
            print("All columns are present in the DataFrame.")
        else:
            print("Not all columns are present in the DataFrame. Exiting ...")
            sys.exit()
    
    def create_sort_date_columns(self):
        self.df = self.df[self.df["instance_date"].str[-4:]>="2010"].copy()
        self.df["day_dt"] = pd.to_datetime(self.df["instance_date"], format='mixed')
        self.df["year_month"] = self.df["day_dt"].dt.to_period('M')
        self.df["year"] = self.df["day_dt"].dt.to_period('Y')
        self.df.sort_values("day_dt", ascending=True, inplace=True)
    
    def filter_columns(self):
        self.columns_of_interest.extend(["day_dt", "year_month", "year"])
        initial_shape = self.df.shape
        self.df = self.df[self.columns_of_interest].copy()
        final_shape = self.df.shape
        print(f"Filtering columns. Shape went from {initial_shape} to {final_shape}.")

    def filter_rows(self):
        initial_shape = self.df.shape
        self.df = self.df[self.df["property_type_en"].isin(["Unit", "Villa"])].copy()
        print(f"After filtering only property_type_en as Unit or Villa, we went from {initial_shape} to {self.df.shape}")
        self.df = self.df[self.df["property_sub_type_en"].isin(["Flat", "Villa"])].copy()
        print(f"After filtering property_sub_type_en as Flat or Villa, the shape is {self.df.shape}")
        self.df.dropna(subset=["rooms_en"], inplace=True)
        print(f"After dropping null values for rooms_en, the shape is {self.df.shape}")
        final_shape = self.df.shape
        print(f"Filtering rows. Shape went from {initial_shape} to {final_shape}.")
    
    def calculate_columns(self):
        self.df["building_name"].fillna(self.df["project_name_en"], inplace=True)
        self.df = self.df[~self.df["building_name"].isna()].copy()
        self.df["address"] = "Dubai, " + self.df["project_name_en"]
        self.df["address"] = self.df["address"].str.lower()
        self.df["building_name"] = self.df["building_name"].str.lower()

    
    def add_coords(self):
        df_building_coords = pd.read_parquet("/Users/luigibungaro/personal/dubai-house-sell-rent-prices/data_preprocessing/data/building_dubai_coords.parquet")
        df_building_coords["building_name"] = df_building_coords["building_name"].str.lower()
        self.df = self.df.merge(df_building_coords, on="building_name", how="left")

    
    def rename_columns(self):
        # Replace values
        self.df["rooms_en"] = self.df["rooms_en"].replace({
            "1 B/R": "1BR",
            "2 B/R": "2BR",
            "3 B/R": "3BR"
        })
        # Rename columns
        self.df = self.df.rename(columns={
            "building_name_en": "building_name",
            "area_name_en": "area",
            "rooms_en": "type"
        })
        


    def process_df(self):
        self.check_columns_in_df()
        self.create_sort_date_columns()
        self.filter_columns()
        self.filter_rows()
        self.rename_columns()
        self.calculate_columns()
        self.add_coords()
        return self.df

class RentTransactions:
    def __init__(self, df):
        self.df = df
        self.columns_of_interest = ["contract_id", "contract_reg_type_en", "contract_start_date", "contract_end_date", "contract_amount", "annual_amount",
                      "ejari_bus_property_type_en", "ejari_property_type_en", "ejari_property_sub_type_en", "property_usage_en", 
                      "project_name_en", "master_project_en", "area_id", "area_name_en", "actual_area", "nearest_landmark_en",
                      "nearest_metro_en", "nearest_mall_en", "tenant_type_en"]
    
    def check_columns_in_df(self):

        if all(col in self.df.columns for col in self.columns_of_interest):
            print("All columns are present in the DataFrame.")
        else:
            print("Not all columns are present in the DataFrame. Exiting ...")
            sys.exit()
    
    def create_sort_date_columns(self):
        self.df["day_dt"] = pd.to_datetime(self.df["contract_start_date"], format='mixed')
        self.df["year_month"] = self.df["day_dt"].dt.to_period('M')
        self.df["year"] = self.df["day_dt"].dt.to_period('Y')
        self.df.sort_values("day_dt", ascending=True, inplace=True)
    
    def filter_columns(self):
        self.columns_of_interest.extend(["day_dt", "year_month", "year"])
        initial_shape = self.df.shape
        self.df = self.df[self.columns_of_interest].copy()
        final_shape = self.df.shape
        print(f"Filtering columns. Shape went from {initial_shape} to {final_shape}.")

    def filter_rows(self):
        initial_shape = self.df.shape
        self.df = self.df[self.df["property_usage_en"]=="Residential"].copy()
        self.df.dropna(subset=["ejari_property_sub_type_en"], inplace=True)
        print(f"After dropping null values for ejari_property_sub_type_en shape from {initial_shape} to {self.df.shape}")
        self.df = self.df[self.df["ejari_property_sub_type_en"].str.contains("bed room")].copy()
        print(f"After filtering only bedroom for ejari_property_sub_type_en shape is {self.df.shape}")
        self.df = self.df[~self.df["annual_amount"].isna()].copy()
        print(f"After dropping null values for annual_amount, the shape is {self.df.shape}")
        self.df = self.df[~self.df["actual_area"].isna()].copy()
        print(f"After dropping null values for actual_area, the shape is {self.df.shape}")
        self.df = self.df[~self.df["project_name_en"].isna()].copy()
        print(f"After dropping null values for project_name_en, the shape is {self.df.shape}")
        final_shape = self.df.shape
        print(f"Filtering rows. Shape went from {initial_shape} to {final_shape}.")
    
    def calculate_columns(self):
        self.df["price_meter"] = self.df["annual_amount"] / self.df["actual_area"]
        
    
    def rename_columns(self):
        # Replace values
        self.df["ejari_property_sub_type_en"] = self.df["ejari_property_sub_type_en"].replace({
            "1bed room+Hall": "1BR",
            "2 bed rooms+hall": "2BR",
            "3 bed rooms+hall": "3BR"
        })
        # Rename columns
        self.df = self.df.rename(columns={
            "project_name_en": "building_name",
            "area_name_en": "area",
            "ejari_property_sub_type_en": "type"
        })
        
    def add_coords(self):                     
        df_building_coords = pd.read_parquet("/Users/luigibungaro/personal/dubai-house-sell-rent-prices/data_preprocessing/data/building_dubai_coords.parquet")
        self.df["building_name"] = self.df["building_name"].str.lower()
        self.df["address"] = "Dubai, " + self.df["building_name"]
        self.df["address"] = self.df["address"].str.lower()
        self.df["building_name"] = self.df["building_name"].str.lower()
        self.df = self.df.merge(df_building_coords, on="building_name", how="left")


    def process_df(self):
        self.check_columns_in_df()
        self.create_sort_date_columns()
        self.filter_columns()
        self.filter_rows()
        self.calculate_columns()
        self.rename_columns()
        self.add_coords()
        return self.df
    
if __name__=="__main__":
    convert_csv_to_parquet(csv_path="/Users/luigibungaro/personal/dubai-house-sell-rent-prices/data_preprocessing/data/Rent_Contracts.csv")
    convert_csv_to_parquet(csv_path="/Users/luigibungaro/personal/dubai-house-sell-rent-prices/data_preprocessing/data/Transactions.csv")

    df = pd.read_parquet("/Users/luigibungaro/personal/dubai-house-sell-rent-prices/data_preprocessing/data/Transactions.parquet")
    df_sell = SellTransactions(df).process_df()
    df_sell.to_parquet("/Users/luigibungaro/personal/dubai-house-sell-rent-prices/data/df_sell.parquet")

    df = pd.read_parquet("/Users/luigibungaro/personal/dubai-house-sell-rent-prices/data_preprocessing/data/Rent_Contracts.parquet")
    df_rent = RentTransactions(df).process_df()
    df_rent.to_parquet("/Users/luigibungaro/personal/dubai-house-sell-rent-prices/data/df_rent.parquet")
    print("finished!")