import streamlit as st
from streamlit.logger import get_logger
import numpy as np
from Hello import duckCon
import plotly.express as px
import pandas as pd


LOGGER = get_logger(__name__)


def run():

  df_monthly_spliy_property = duckCon.execute("select * from main_golden.monthly_split_property").fetch_df()
  df_monthly_spliy_property['year_month'] = pd.to_datetime(df_monthly_spliy_property['year_month'], format='%Y%m')
  df_monthly_spliy_property = df_monthly_spliy_property.sort_values(by='year_month')
  df_monthly_split_regtype = duckCon.execute("select * from main_golden.monthly_split_regtype").fetch_df()

  # Create the plot
  fig_property = px.line(
        df_monthly_spliy_property, 
        x='year_month', 
        y='num_contracts',  # Ensure it's a single y-column, no list
        color='property_type',  # Split the lines based on property_type_en
        labels={
            'year_month': 'Year-Month',
            'num_contracts': 'Num Contracts Count',
            'property_type_en': 'Property Type'
        },
        title="Monthly Rolling Sales Values by Property Type"
    )
  # Increase the size of the graph
  fig_property.update_layout(
      width=1000,  # Increase width
      height=600,  # Increase height
      title_font_size=20,  # Optional: increase title size
      xaxis_title_font_size=16,  # Optional: increase x-axis title size
      yaxis_title_font_size=16  # Optional: increase y-axis title size
  )

#   # Create the plot
#   fig_prop_type = px.line(df_monthly_rolling, 
#                 x='year_month', 
#                 y=['rolling_12_month_num_sales_villa', 
#                     'rolling_12_month_num_sales_unit',
#                   'total_sales'], 
#                 labels={
#                     'year_month': 'Year-Month',
#                     'value': 'Sales Count',
#                     'variable': 'Rolling Metrics'
#                 },
#                 title="Monthly Rolling Sales Values by Property Type")
#   # Increase the size of the graph
#   fig_prop_type.update_layout(
#       width=1000,  # Increase width
#       height=600,  # Increase height
#       title_font_size=20,  # Optional: increase title size
#       xaxis_title_font_size=16,  # Optional: increase x-axis title size
#       yaxis_title_font_size=16  # Optional: increase y-axis title size
#   )



#   with st.container():
#     st.title("Dubai House Rent and Sales Prices Report")
#   with st.container():
#     col_villa, col_unit = st.columns(2)
#     with col_villa:
#       st.header("Villa")
#       st.markdown("#### Off-Plan to Existing space Growth Rate")
#       sqm_existing = round(df_villa_offplan_area_price.iloc[0,1],0)
#       sqm_offplan = round(df_villa_offplan_area_price.iloc[1,1],1)
#       sqm_offplan_vs_existing = round( (sqm_offplan-sqm_existing)/sqm_existing * 100, 1)
#       st.metric(label="", value=f"{sqm_offplan} m2", delta=f"{sqm_offplan_vs_existing} %")

#       st.markdown("#### Off-Plan to Existing price/sqm Growth Rate")
#       sqm_price_existing = round(df_villa_offplan_area_price.iloc[0,2],0)
#       sqm_price_offplan = round(df_villa_offplan_area_price.iloc[1,2],0)
#       sqm_price_offplan_vs_existing = round( (sqm_price_offplan - sqm_price_existing)/sqm_price_existing * 100, 1)
#       st.metric(label="", value=f"{sqm_price_offplan} AED/m2", delta=f"{sqm_price_offplan_vs_existing} %")
#     with col_unit:
#       st.header("Unit")
#       st.markdown("#### Off-Plan to Existing space Growth Rate")
#       sqm_existing = round(df_unit_offplan_area_price.iloc[0,1],0)
#       sqm_offplan = round(df_unit_offplan_area_price.iloc[1,1],1)
#       sqm_offplan_vs_existing = round( (sqm_offplan-sqm_existing)/sqm_existing * 100, 1)
#       st.metric(label="", value=f"{sqm_offplan} m2", delta=f"{sqm_offplan_vs_existing} %")

#       st.markdown("#### Off-Plan to Existing price/sqm Growth Rate")
#       sqm_price_existing = round(df_unit_offplan_area_price.iloc[0,2],0)
#       sqm_price_offplan = round(df_unit_offplan_area_price.iloc[1,2],0)
#       sqm_price_offplan_vs_existing = round( (sqm_price_offplan - sqm_price_existing)/sqm_price_existing * 100, 1)
#       st.metric(label="", value=f"{sqm_price_offplan} AED/m2", delta=f"{sqm_price_offplan_vs_existing} %")

  # Customize hover data to show values on hover
  st.header("Monthly  by Registration Type: Off-Plan vs Existing")
  fig_property.update_traces(mode="lines+markers", hovertemplate='%{x}<br>SalContContractsractses: %{y}<extra></extra>')

  # Add chart to Streamlit app
  st.plotly_chart(fig_property)

#   st.header("Rolling Sales by Property Type: Villa vs Unit")
#   fig_prop_type.update_traces(mode="lines+markers", hovertemplate='%{x}<br>Sales: %{y}<extra></extra>')

#   # Add chart to Streamlit app
#   st.plotly_chart(fig_prop_type)


if __name__ == "__main__":
    run()
