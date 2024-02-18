import streamlit as st
from streamlit.logger import get_logger
import numpy as np

LOGGER = get_logger(__name__)



def run():
    st.set_page_config(
        page_title="Home",
        page_icon="👋",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.write("# Welcome to Dubai House Rent and Sales Prices Report")
    st.write("### Data source: Dubai open datasets from Pulse")
    st.markdown("#### [contact me](https://www.tapnkonnect.com/profile_view/713)")
    st.image("assets/dubai.jpg")
    st.balloons()
  

if __name__ == "__main__":
    run()
