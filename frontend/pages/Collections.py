import streamlit as st
import datetime
import pandas as pd
from utils import get_all_device_ids, get_device_data, get_device_fields
from constants import device_type_labels, device_checkbox_labels


st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.header('Lipo Solar Analysis')
### DEVICE TYPE SELECTION
device_type_label = st.sidebar.selectbox('Device', tuple(device_type_labels.keys())) 
device_type = device_type_labels[device_type_label].value

### DEVICE ID SELECTION
@st.cache_data
def get_all_device_ids_cached(device_type_value):
    return get_all_device_ids(device_type_value)

device_id_options = ()
if device_type_label:
    device_ids = get_all_device_ids_cached(device_type)
    device_id_options = tuple(sorted(device_ids))

device_id = st.sidebar.selectbox(device_checkbox_labels[device_type_label], device_id_options) 

### DATE RANGE SELECTION
current_time = datetime.datetime.now()
default_start_time = current_time - datetime.timedelta(days=14)
date_range = st.sidebar.date_input(
    "From",
    (default_start_time, current_time),
    None,
    current_time,
    format="MM.DD.YYYY",
)
### FIELDS MULTI_SELECTION
if device_type_label:
    device_fields = get_device_fields(device_type)
    device_fields_options = tuple(sorted(device_fields))
st.sidebar.subheader('Fields')
data_fields = st.sidebar.multiselect('Select fields', device_fields_options, ['state_of_charge'])

# @st.cache_data
def get_device_data_cached(*arg):
    return get_device_data(*arg)
device_data = None
if st.sidebar.button("Update",  type="primary"):
    start_time = datetime.datetime.combine(date_range[0], datetime.time.min)
    end_time = datetime.datetime.combine(date_range[1], datetime.time.max)
    device_data = get_device_data_cached(device_type, 
                                         device_id, data_fields, 
                                         start_time.timestamp(), 
                                         end_time.timestamp()
                                        )


st.markdown(f'## {device_type_label}: {device_id}')

# Row B
seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])

# Row C
if device_data:
    data = device_data['data']
    st.line_chart(data, x = 'ts', y = data_fields, height = 500)