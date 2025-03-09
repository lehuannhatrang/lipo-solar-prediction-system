import streamlit as st

def set_page_config() -> None:
    if 'page_config_set' not in st.session_state:
        st.set_page_config(layout="wide", initial_sidebar_state='expanded')
        st.session_state.page_config_set = True