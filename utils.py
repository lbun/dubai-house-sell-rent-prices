# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import streamlit as st


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
    group_rent = df_rent_filtered.groupby(["area", "building_name", "address", "year", "address_year"]).agg({"annual_amount":"median", "price_meter":"count"})\
        .reset_index().rename(columns={"price_meter": "num_rent_contracts"})
    # Creating groupby for sell
    group_sell = df_sell_filtered.groupby(["address_year"]).agg({"actual_worth":"median", "year":"count"})\
        .reset_index().rename(columns={"year": "num_sales", "actual_worth": "median_sale_price"})
    # Merging the 2 groups
    group_all = group_rent.merge(group_sell, on="address_year", how="left")
    group_all.dropna(subset=["median_sale_price", "num_sales"], inplace=True)
    group_all["roi_years"] = group_all["median_sale_price"]/group_all["annual_amount"]
    return group_all.sort_values("roi_years", ascending=True)