import pandas as pd
import streamlit as st
import datetime

@st.cache_data
def load_rent_df():
    df = pd.read_parquet("data/df_rent.parquet")
    df["year"] = df["year"].astype(str)
    df = df[df["type"].isin(["1BR", "2BR", "3BR"])]

    return df.drop(columns=["contract_id", "contract_reg_type_en", "property_usage_en", "tenant_type_en", "day_dt", "master_project_en"])

@st.cache_data
def load_sell_df():
    df = pd.read_parquet("data/df_sell.parquet")
    df["year"] = df["year"].astype(str)
    df["day_dt"] = pd.to_datetime(df["day_dt"])
    df = df[df["type"].isin(["1BR", "2BR", "3BR"])]

    return df

@st.cache_data
def calculate_roi(df_rent, df_sell):
    common_addresses = list(set(df_sell["address"].unique()) & set(df_rent["address"].unique()))
    # Filtering df_rent
    df_rent_filtered = df_rent[df_rent["address"].isin(common_addresses)].copy()
    df_rent_filtered["address_year"] = df_rent_filtered["address"] + "_" + df_rent_filtered["year"].astype(str)
    # Filtering df_sell
    df_sell_filtered = df_sell[df_sell["address"].isin(common_addresses)].copy()
    df_sell_filtered["address_year"] = df_sell_filtered["address"] + "_" + df_sell_filtered["year"].astype(str)
    # Creating groupby for rent
    group_rent = df_rent_filtered.groupby(["area", "building_name", "address", "year", "address_year"])\
        .agg(num_rent_contracts=("price_meter", "count"), annual_amount=("annual_amount", "median")).reset_index()
    # Creating groupby for sell
    group_sell = df_sell_filtered.groupby(["address_year"]).agg(median_sale_price=("actual_worth", "median"), num_sales=("year", "count")).reset_index()
    # Merging the 2 groups
    group_all = group_rent.merge(group_sell, on="address_year", how="left")
    group_all.dropna(subset=["median_sale_price", "num_sales"], inplace=True)
    group_all["roi_years"] = group_all["median_sale_price"]/group_all["annual_amount"]
    return group_all.sort_values("roi_years", ascending=True)

@st.cache_data
def calculate_roi_by(df_roi, by_col="area"):
    # Group by 'year' and 'area' and calculate count and median
    df_roi.sort_values([by_col, "year"], ascending=True, inplace=True)
    grouped_df = df_roi.groupby([by_col, 'year']).agg(
        num_rent_contracts=('num_rent_contracts', 'sum'),
        num_sales=('num_sales', 'sum'), 
        median_sale_price=('median_sale_price', 'median'),
        median_rent_price=('annual_amount', 'median'),
        roi_median=('roi_years', 'median')
        ).reset_index()

    # Group by 'area' and create a new DataFrame with lists of values
    result_df = grouped_df.groupby(by_col).agg(
        num_rent_contracts_list=('num_rent_contracts', list), 
        num_sell_contracts_list=('num_sales', list), 
        median_sale_price_list=('median_sale_price', list),
        median_rent_price_list=('median_rent_price', list),
        roi_median_list=('roi_median', list)
        ).reset_index()
    result_df['num_rent_contracts_list'] = result_df['num_rent_contracts_list'].apply(lambda x: [int(num) for num in x])
    result_df['num_sell_contracts_list'] = result_df['num_sell_contracts_list'].apply(lambda x: [int(num) for num in x])
    return result_df

if __name__=="__main__":
    df_rent = load_rent_df()
    df_sell = load_sell_df()
    group_all = calculate_roi(df_rent, df_sell)

    df_roy_by_area = calculate_roi_by(group_all, by_col="area")
    df_roy_by_building = calculate_roi_by(group_all, by_col="building_name")
    print("finished")