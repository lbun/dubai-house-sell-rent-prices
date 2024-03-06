import time
import numpy as np
import pandas as pd
import streamlit as st
from streamlit.hello.utils import show_code
from utils import load_rent_df
import plotly.express as px
import datetime

def plotting_num_transactions():
    st.set_page_config(
        page_title="Yearly Transactions",
        layout="wide"
    )
    df = load_rent_df()

    months_list = []
    today = datetime.datetime.now()
    for i in range(1,25):
        year_month = (datetime.datetime(today.year, today.month, 1) - datetime.timedelta(20*i)).strftime("%Y-%m")
        months_list.append(year_month)
    # plotting only last year data
    df["year_month"] = df["year_month"].astype(str)
    group_area_1y = df[df["year_month"].isin(months_list)].groupby(["year_month", "type"])["year"].count().reset_index()
    group_area_1y["year_month"] = pd.to_datetime(group_area_1y["year_month"].astype(str))


    # Create an interactive line plot using plotly express
    fig1 = px.line(group_area_1y,
                x='year_month', y='year', color='type', markers=True,
                title='Last 2 years Transactions', labels={'year_month': 'Num transactions'})
    fig1.update_layout(width=1400, height=400)

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig1)



    group_area = df.groupby(["year", "type"])["year_month"].count().reset_index()
    group_area["year"] = pd.to_datetime(group_area["year"].astype(str))
    group_area.head(2)

    # Create an interactive line plot using plotly express
    fig2 = px.line(group_area,
                x='year', y='year_month', color='type', markers=True,
                title='Num transactions Over Time', labels={'year_month': 'Num transactions'})
    fig2.update_layout(width=1400, height=400)

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig2)

    

plotting_num_transactions()

    