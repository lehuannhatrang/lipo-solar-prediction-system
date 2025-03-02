import streamlit as st
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

from authentication import check_authenticate
from components.user_profile.index import user_profile
from utils import render_sidebar_navigation
from utils_i18n.i18n import get_text

check_authenticate()

render_sidebar_navigation()
    
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
# user_profile()

# Row A
st.markdown(f'## {get_text("home.title")}')
st.markdown(f'### {get_text("home.liBattery")}')
col1, col2 = st.columns(2)
col1.metric(get_text("home.total"), "10", "1")
col2.metric(get_text("home.anomaly"), "0", "-1")

st.markdown(f'### {get_text("home.solarPanel")}')
col1, col2 = st.columns(2)
col1.metric(get_text("home.total"), "100", "22")
col2.metric(get_text("home.anomaly"), "3", "2")