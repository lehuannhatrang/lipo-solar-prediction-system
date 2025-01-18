import streamlit as st
import datetime
import pandas as pd
import random
import matplotlib.colors as mcolors
from authentication import check_authenticate
from components.user_profile.index import user_profile
from utils import get_all_device_ids, get_device_data, get_device_fields, render_sidebar_navigation
from constants import device_type_labels, device_checkbox_labels, chart_colour

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

check_authenticate()

render_sidebar_navigation()

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
user_profile()

st.sidebar.header('Collections')

if 'query_data' not in st.session_state:
    st.session_state.query_data = None
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
    "From - To",
    (default_start_time, current_time),
    None,
    current_time,
    format="MM.DD.YYYY",
)
### FIELDS MULTI_SELECTION
@st.cache_data
def get_device_fields_cached(*arg):
    return get_device_fields(*arg)

if device_type_label:
    device_fields = get_device_fields_cached(device_type)
    if 'ts' in device_fields:
        device_fields_options = ['ts'] + sorted([field for field in device_fields if field != 'ts'])
    else:
        device_fields_options = tuple(sorted(device_fields))

st.sidebar.subheader('Chart options')

x_axis_field = st.sidebar.selectbox('X Axis', tuple(device_fields_options))

y_axis_fields_options = filter(lambda x: x not in x_axis_field, device_fields)
y_axis_fields = st.sidebar.multiselect('Y Axis', tuple(y_axis_fields_options))



@st.cache_data
def get_device_data_cached(*arg):
    return get_device_data(*arg)

def allow_submit():
    return bool(device_id) and \
           date_range and len(date_range) >= 2 and date_range[0] and date_range[1] and \
           y_axis_fields and len(y_axis_fields) > 0

if st.sidebar.button("Update",  type="primary", disabled=not allow_submit()):
    start_time = datetime.datetime.combine(date_range[0], datetime.time.min)
    end_time = datetime.datetime.combine(date_range[1], datetime.time.max)
    data_fields = [x_axis_field] + y_axis_fields
    device_data = get_device_data_cached(device_type, 
                                         device_id, data_fields, 
                                         start_time.timestamp(), 
                                         end_time.timestamp()
                                        )
    st.session_state.query_data = {
        "data_fields": data_fields,
        "device_id": device_id,
        "device_type_label": device_type_label,
        "device_data": device_data,
        "x_axis_field": x_axis_field,
        "y_axis_fields": y_axis_fields
    }

### RENDER page
if st.session_state.query_data:
    device_id, data_fields, device_type_label, device_data, x_axis_field, y_axis_fields = (
        st.session_state.query_data["device_id"],
        st.session_state.query_data["data_fields"],
        st.session_state.query_data["device_type_label"],
        st.session_state.query_data["device_data"],
        st.session_state.query_data["x_axis_field"],
        st.session_state.query_data["y_axis_fields"],
    )

    st.markdown(f'## {device_type_label}: {device_id}')
    # Row C
    if device_data:
        data = device_data['data']
        if x_axis_field == 'ts':
            data = pd.DataFrame(data)
            data['datetime'] = pd.to_datetime(data['ts'])
            x_axis_field = 'datetime'
        colour = chart_colour
        if len(y_axis_fields) > len(colour):
            colour = colour  + [mcolors.to_hex([random.random(), random.random(), random.random()]) for _ in range(len(y_axis_fields) - len(colour))]
        color_list = colour[:len(y_axis_fields)]
        st.line_chart(data, x = x_axis_field, y = y_axis_fields, height = 500, color=(color_list))