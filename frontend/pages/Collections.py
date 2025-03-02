import streamlit as st
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

import datetime
import pandas as pd
import random
import matplotlib.colors as mcolors
from authentication import check_authenticate
from components.user_profile import user_profile
from utils import get_all_device_ids, get_device_data, get_device_fields, render_sidebar_navigation
from utils_i18n.i18n import get_text
from constants import device_type_labels, chart_colour


check_authenticate()

render_sidebar_navigation()

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
user_profile()

st.sidebar.header(get_text('collections.title'))

include_customer_entity = st.sidebar.checkbox(get_text('common.includeCustomer'), value=True)

if 'query_data' not in st.session_state:
    st.session_state.query_data = None
### DEVICE TYPE SELECTION
device_type_label = st.sidebar.selectbox(get_text('common.device'), tuple(device_type_labels.keys())) 
device_type = device_type_labels[device_type_label].value

### DEVICE ID SELECTION
@st.cache_data
def get_all_device_ids_cached(*args):
    return get_all_device_ids(*args)

device_name_options = ()
if device_type_label:
    device_infos = get_all_device_ids_cached(device_type, include_customer_entity)
    device_names = [device_info['name'] for device_info in device_infos]
    device_name_options = tuple(sorted(device_names))

device_name = st.sidebar.selectbox(get_text('common.deviceName'), device_name_options)
if device_name:
    device_id = [device_info['id'] for device_info in device_infos if device_info['name'] == device_name]
    if len(device_id) > 1:
        device_id = st.sidebar.selectbox(get_text('common.deviceId'), device_id, disabled=(len(device_id) == 1))
    else:
        device_id = device_id[0]
        st.sidebar.markdown(f"{get_text('common.deviceId')}: {device_id}")

### FIELDS MULTI_SELECTION
@st.cache_data
def get_device_fields_cached(*arg):
    return get_device_fields(*arg)

if device_id:
    device_fields = get_device_fields_cached(device_id)
    if 'timestamp' in device_fields:
        device_fields_options = ['timestamp'] + sorted([field for field in device_fields if field != 'timestamp'])
    else:
        device_fields_options = sorted(device_fields)

    x_axis_field = st.sidebar.selectbox(get_text('collections.xAxis'), device_fields_options)
    y_axis_fields = st.sidebar.multiselect(get_text('collections.yAxis'), device_fields_options)

### DATE RANGE SELECTION
current_time = datetime.datetime.now()
default_start_time = current_time - datetime.timedelta(days=14)
date_range = st.sidebar.date_input(get_text('collections.dateRange'), value=(default_start_time, current_time))

@st.cache_data
def get_device_data_cached(*arg):
    return get_device_data(*arg)

def allow_submit():
    return (
        device_id is not None and
        x_axis_field is not None and
        len(y_axis_fields) > 0 and
        len(date_range) == 2 and
        date_range[0] is not None and
        date_range[1] is not None
    )

if st.sidebar.button(get_text('common.update'), type="primary", disabled=not allow_submit()):
    start_time = datetime.datetime.combine(date_range[0], datetime.time.min)
    end_time = datetime.datetime.combine(date_range[1], datetime.time.max)
    data_fields = [x_axis_field] + y_axis_fields
    data = get_device_data_cached(device_type, device_id, data_fields, start_time.timestamp(), end_time.timestamp())
    st.session_state.query_data = {
        "data_fields": data_fields,
        "device_id": device_id,
        "device_name": device_name,
        "device_type_label": device_type_label,
        "device_data": data,
        "x_axis_field": x_axis_field,
        "y_axis_fields": y_axis_fields
    }

### RENDER page
if st.session_state.query_data:
    device_id, device_name, data_fields, device_type_label, device_data, x_axis_field, y_axis_fields = (
        st.session_state.query_data["device_id"],
        st.session_state.query_data["device_name"],
        st.session_state.query_data["data_fields"],
        st.session_state.query_data["device_type_label"],
        st.session_state.query_data["device_data"],
        st.session_state.query_data["x_axis_field"],
        st.session_state.query_data["y_axis_fields"],
    )

    st.markdown(f'## {device_type_label}: {device_name}')
    # Row C
    if device_data:
        data = device_data['data']
        if len(data) > 0:
            if x_axis_field == 'timestamp':
                data = pd.DataFrame(data)
                data['datetime'] = pd.to_datetime(data['timestamp'])
                x_axis_field = 'datetime'
            colour = chart_colour
            if len(y_axis_fields) > len(colour):
                colour = colour  + [mcolors.to_hex([random.random(), random.random(), random.random()]) for _ in range(len(y_axis_fields) - len(colour))]
            color_list = colour[:len(y_axis_fields)]
            st.line_chart(data, x = x_axis_field, y = y_axis_fields, height = 500, color=(color_list))
        else:
            st.image("gallery/images/data_not_found.jpg", width=800)
            st.warning(get_text('collections.noData'))
else:
    st.markdown(get_text('collections.selectParams'))
