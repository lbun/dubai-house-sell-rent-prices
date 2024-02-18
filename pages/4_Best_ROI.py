import numpy as np
import streamlit as st
from utils import load_rent_df, load_sell_df, calculate_roi, calculate_roi_by
import plotly.express as px

def display_page():
    st.set_page_config(
        page_title="Best ROI areas and buildings",
        layout="wide"
    )
    st.write("# Best ROI areas and buildings")
    df_rent = load_rent_df()
    df_sell = load_sell_df()

    dubai_areas = sorted(df_rent["area"].unique().tolist())
    dubai_buildings = sorted(df_rent["building_name"].unique().tolist())
    years = sorted(df_rent["year"].unique().tolist())[::-1]
    builing_type = sorted(df_rent["type"].unique().tolist())


    st.write("### Select desired Area of Dubai, or building name, or building type (1BR, 2BR and 3BR) or specific year of interest")
    st.write("These data are collected from Dubai open Dataset (Dubai Pulse that has also historical data)")

    with st.container():
      col1, col2, col3, col4 = st.columns(4)
      with col1:
        selected_areas = st.multiselect(label="Area", options=dubai_areas)
      with col2:
        seleceted_buildings = st.multiselect(label="Building Name", options=dubai_buildings)
      with col3:
        seleceted_building_type = st.multiselect(label="Building Type", options=builing_type)
      with col4:
        seleceted_years = st.multiselect(label="Year", options=years)
    
    if selected_areas:
        df_rent = df_rent[df_rent["area"].isin(selected_areas)]
        df_sell = df_sell[df_sell["area"].isin(selected_areas)]
    if seleceted_buildings:
        df_rent = df_rent[df_rent["building_name"].isin(seleceted_buildings)]
        df_sell = df_sell[df_sell["building_name"].isin(seleceted_buildings)]
    if seleceted_years:
        df_rent = df_rent[df_rent["year"].isin(seleceted_years)]
        df_sell = df_sell[df_sell["year"].isin(seleceted_years)]
    if seleceted_building_type:
        df_rent = df_rent[df_rent["type"].isin(seleceted_building_type)]
        df_sell = df_sell[df_sell["type"].isin(seleceted_building_type)]

    group_all = calculate_roi(df_rent=df_rent, df_sell=df_sell)
    df_roy_by_area = calculate_roi_by(group_all, by_col="area")
    df_roy_by_building = calculate_roi_by(group_all, by_col="building_name")

    # Create a histogram with Plotly Express
    fig = px.histogram(group_all[group_all["roi_years"] < 20], x="roi_years", nbins=20, title="Distribution of ROI Years")

    # Customize figure size
    fig.update_layout(width=1200, height=400)
    st.plotly_chart(fig)
    st.write("Summary data by Area")
    st.data_editor(
    df_roy_by_area,
    column_config={
        "num_sell_contracts_list": st.column_config.BarChartColumn(
            "trend number of sales by year",
            help="The number of sales by year for area",
            y_min=0,
            y_max=str(df_roy_by_area["num_sell_contracts_list"].apply(lambda x: max(x)).max()),
        ),
        "num_rent_contracts_list": st.column_config.BarChartColumn(
            "Trend number of contracts by year",
            help="The number of contracts by year for area",
            y_min=0,
            y_max=str(df_roy_by_area["num_rent_contracts_list"].apply(lambda x: max(x)).max()),
        ),
            "median_sale_price_list": st.column_config.LineChartColumn(
            "Trend Sale Price year",
            width="medium",
            help="Median of sale price by year",
            y_min=0,
            y_max=df_roy_by_building["median_sale_price_list"].apply(lambda x: max(x)).quantile(0.75),
         ),
         "median_rent_price_list": st.column_config.LineChartColumn(
            "Trend rent price by year",
            width="medium",
            help="Median of rent price by year",
            y_min=0,
            y_max=df_roy_by_building["median_rent_price_list"].apply(lambda x: max(x)).quantile(0.75),
         ),
        "roi_median_list": st.column_config.LineChartColumn(
            "Trend median roi by year",
            width="medium",
            help="The median roi by year",
            y_min=0,
            y_max=20,
         ),
    },


    hide_index=True,
    )
    st.write("Summary data by Building")
    st.data_editor(
    df_roy_by_building,
    column_config={
        "num_sell_contracts_list": st.column_config.BarChartColumn(
            "trend number of sales by year",
            help="The number of sales by year for area",
            y_min=0,
            y_max=str(df_roy_by_building["num_sell_contracts_list"].apply(lambda x: max(x)).max()),
        ),
        "num_rent_contracts_list": st.column_config.BarChartColumn(
            "Trend number of contracts by year",
            help="The number of contracts by year for area",
            y_min=0,
            y_max=str(df_roy_by_building["num_rent_contracts_list"].apply(lambda x: max(x)).max()),
        ),
        "median_sale_price_list": st.column_config.LineChartColumn(
            "Trend Sale Price year",
            width="medium",
            help="Median of sale price by year",
            y_min=0,
            y_max=df_roy_by_building["median_sale_price_list"].apply(lambda x: max(x)).quantile(0.75),
         ),
         "median_rent_price_list": st.column_config.LineChartColumn(
            "Trend rent price by year",
            width="medium",
            help="Median of rent price by year",
            y_min=0,
            y_max=df_roy_by_building["median_rent_price_list"].apply(lambda x: max(x)).quantile(0.75),
         ),
        "roi_median_list": st.column_config.LineChartColumn(
            "Trend median roi by year",
            width="medium",
            help="The median roi by year",
            y_min=0,
            y_max=20,
         ),
    },


    hide_index=True,
    )


    st.dataframe(group_all)


display_page()