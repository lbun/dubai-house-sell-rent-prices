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

import streamlit as st
from streamlit.logger import get_logger
from utils import load_rent_df
import numpy as np

LOGGER = get_logger(__name__)


def filter_year(df, year):
    return df[df["year"]==year] 

def run():
    st.set_page_config(
        page_title="Home",
        page_icon="👋",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    df = load_rent_df()

    dubai_areas = sorted(df["area"].unique().tolist())
    dubai_buildings = sorted(df["building_name"].unique().tolist())
    years = sorted(df["year"].unique().tolist())[::-1]
    builing_type = sorted(df["type"].unique().tolist())

    st.write("# Insights on Dubai House prices (Buy and Rent)!")

    st.write("### Rent Transactions. Select desired Area of Dubai, or building name, or building type (1BR, 2BR and 3BR) or specific year of interest")
    st.write("These data are collected from Dubai open Dataset (Dubai Pulse that has also historical data)")
    st.write("You can select the building of interest and see at what price the last contracts were signed)")


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


    st.sidebar.success("Select page here.")


    with st.container():
      rows_per_page = 1000
      total_pages = (len(df)-1) // rows_per_page + 1
      # Get the current page number from the user
      page_number = st.multiselect(label="Page Number", options=list(np.arange(1,total_pages, 1)))
      #page_number = st.slider("Select Page", 1, total_pages, 1)
      if not page_number:
         page_number = [1]

      start_index = (int(page_number[0]) - 1) * rows_per_page
      end_index = min(int(page_number[0]) * rows_per_page, len(df))
      if selected_areas:
        df = df[df["area"].isin(selected_areas)]
      if seleceted_buildings:
        df = df[df["building_name"].isin(seleceted_buildings)]
      if seleceted_years:
          df = df[df["year"].isin(seleceted_years)]
      if seleceted_building_type:
          df = df[df["type"].isin(seleceted_building_type)]
      st.dataframe(
          df.iloc[start_index:end_index]
      )


if __name__ == "__main__":
    run()
