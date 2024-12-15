import streamlit as st
import pandas as pd
import plost

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    

# Row A
st.markdown('## Dashboards')
st.markdown('### Li-ion Battery')
col1, col2= st.columns(2)
col1.metric("Total", "10", "1")
col2.metric("Anomaly", "0", "-1")

st.markdown('### Solar Panel')
col1, col2= st.columns(2)
col1.metric("Total", "100", "22")
col2.metric("Anomaly", "3", "2")