import streamlit as st
from utils import set_page_config

# set_page_config()

import datetime
import pandas as pd
from authentication import check_authenticate
from components.user_profile.index import user_profile
from utils import get_all_device_ids, render_sidebar_navigation, request_forecast, get_device_fields, get_forecast_data
from utils.i18n import get_text
from utils.prediction import get_rul_predict_fields, request_rul_predictor, get_rul_predict_data
from constants import device_type_labels, forecast_predict_fields, forecast_labels
import plotly.graph_objects as go


check_authenticate()

render_sidebar_navigation()

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

user_profile()


st.sidebar.header(get_text('RulPrediction.title'))

include_customer_entity = st.sidebar.checkbox(get_text('common.includeCustomer'), value=True)

if 'predict_data' not in st.session_state:
    st.session_state.predict_data = None
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

device_name = st.sidebar.selectbox(get_text('forecast.deviceName'), device_name_options)
if device_name:
    device_id = [device_info['id'] for device_info in device_infos if device_info['name'] == device_name]
    if len(device_id) > 1:
        device_id = st.sidebar.selectbox(get_text('forecast.deviceId'), device_id, disabled=(len(device_id) == 1))
    else:
        device_id = device_id[0]
        st.sidebar.markdown(f'{get_text("forecast.deviceId")}: {device_id}')

### FIELDS MULTI_SELECTION
@st.cache_data
def get_device_fields_cached(*arg):
    return get_device_fields(*arg)

if device_id:
    device_fields = get_device_fields_cached(device_id)
    predict_field = get_rul_predict_fields(device_type, device_fields)

def allow_submit():
    return bool(device_id) and bool(predict_field)

if st.sidebar.button(get_text('forecast.update'),  type="primary", disabled=not allow_submit()):
    request = request_rul_predictor(device_type, device_id, device_name, predict_field)
    if "job_id" in request:
        job_id = request["job_id"]
        st.query_params.from_dict({
            "job_id": job_id,
            "predict_field": predict_field,
            "device_id": device_id,
            "device_name": device_name,
            "device_type": device_type,
        })
    else:
        st.error(f'{get_text("rul_request.error")}: {request["message"]}')

@st.cache_data
def get_rul_predict_data_cache(*arg):
    return get_rul_predict_data(*arg)

if 'job_id' in st.query_params:
    job_id = st.query_params.job_id
    with st.spinner(get_text('forecast.waiting')):
        predict_data = get_rul_predict_data_cache(job_id)
        st.session_state.predict_data = predict_data
        if predict_data["predict_data"] == None:
            get_rul_predict_data_cache.clear()


### RENDER page
if  st.session_state.predict_data:
    predict_data= st.session_state.predict_data

    job_status = predict_data['status']
    if job_status == "Success":
        st.success(get_text('forecast.success'))
    else:
        st.warning(get_text('forecast.inProgress'))

    job_metadata = predict_data["job_metadata"]
    
    # st.markdown(f'## {job_metadata["device_type"]}: {job_metadata["device_name"]}')
    
    if predict_data["predict_data"]:
        # Extract actual data and forecast data
        rul_data = predict_data["predict_data"]['rul_prediction']
        st.write(rul_data)
else:
    st.markdown(get_text('forecast.selectParams'))