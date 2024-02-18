import pandas as pd
import streamlit as st
from utils import load_rent_df
import plotly.express as px
import datetime

def rent_price_overtime():
    st.set_page_config(
        page_title="Rent Price Overtime",
        layout="wide"
    )
    df = load_rent_df()

    dubai_areas = sorted(df["area"].unique().tolist())
    dubai_buildings = sorted(df["building_name"].unique().tolist())
    years = sorted(df["year"].unique().tolist())[::-1]
    builing_type = sorted(df["type"].unique().tolist())

    st.write("# Rent Price")

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
        df = df[df["area"].isin(selected_areas)]
    if seleceted_buildings:
        df = df[df["building_name"].isin(seleceted_buildings)]
    if seleceted_years:
        df = df[df["year"].isin(seleceted_years)]
    if seleceted_building_type:
        df = df[df["type"].isin(seleceted_building_type)]

    months_list = []
    today = datetime.datetime.now()
    for i in range(1,25):
        year_month = (datetime.datetime(today.year, today.month, 1) - datetime.timedelta(30*i)).strftime("%Y-%m")
        months_list.append(year_month)
    # plotting only last year data
    df["year_month"] = df["year_month"].astype(str)
    group_median_price = df[df["year_month"].isin(months_list)].groupby("year_month").agg({"annual_amount":"median", "year":"count"}).reset_index()
    group_median_price["year_month"] = pd.to_datetime(group_median_price["year_month"].astype(str))


    # Create an interactive line plot using plotly express
    group_median_price.rename(columns={"year":"num_transactions"}, inplace=True)
    fig_price = px.line(group_median_price,
                x='year_month', y='annual_amount', markers=True,
                title='Median Price Transactions', labels={'annual_amount': 'Median Rent Price'}, hover_data=["num_transactions"])
    fig_price.update_layout(width=1400, height=400)

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig_price)

    
    st.dataframe(df.sort_values("contract_end_date", ascending=False).head(200))

rent_price_overtime()
