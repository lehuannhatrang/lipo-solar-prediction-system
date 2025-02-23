import streamlit as st
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

import datetime
import pandas as pd
from authentication import check_authenticate
from components.user_profile.index import user_profile
from utils import get_all_device_ids, render_sidebar_navigation, request_forecast, get_device_fields, get_forecast_data
from constants import device_type_labels, device_checkbox_labels, forecast_predict_fields, forecast_labels
import plotly.graph_objects as go


check_authenticate()

render_sidebar_navigation()

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

user_profile()
    
st.sidebar.header('Forecast')

if 'predict_data' not in st.session_state:
    st.session_state.predict_data = None
### DEVICE TYPE SELECTION
device_type_label = st.sidebar.selectbox('Device', tuple(device_type_labels.keys())) 
device_type = device_type_labels[device_type_label].value

### DEVICE ID SELECTION
@st.cache_data
def get_all_device_ids_cached(device_type_value):
    return get_all_device_ids(device_type_value)

device_name_options = ()
if device_type_label:
    device_infos = get_all_device_ids_cached(device_type)
    device_names = [device_info['name'] for device_info in device_infos]
    device_name_options = tuple(sorted(device_names))

device_name = st.sidebar.selectbox(device_checkbox_labels[device_type_label], device_name_options)
if device_name:
    device_id = [device_info['id'] for device_info in device_infos if device_info['name'] == device_name]
    if len(device_id) > 1:
        device_id = st.sidebar.selectbox('Device ID', device_id, disabled=(len(device_id) == 1))
    else:
        device_id = device_id[0]
        st.sidebar.markdown(f'Device ID: {device_id}')

### FIELDS MULTI_SELECTION
@st.cache_data
def get_device_fields_cached(*arg):
    return get_device_fields(*arg)

if device_id:
    device_fields = get_device_fields_cached(device_id)
    predict_field_options = list(filter(lambda x: x in forecast_predict_fields, device_fields))

predict_field = st.sidebar.selectbox('Predict field', tuple(predict_field_options))


### DATE RANGE SELECTION
current_time = datetime.datetime.now()
default_start_time = current_time - datetime.timedelta(days=14)
forecast_range_label = st.sidebar.selectbox('Forecast for the next', tuple(forecast_labels.keys()))


def allow_submit():
    return bool(device_id) and bool(predict_field) and bool(forecast_range_label)

if st.sidebar.button("Update",  type="primary", disabled=not allow_submit()):
    forecast_range = forecast_labels[forecast_range_label]
    request = request_forecast(device_type, device_id, device_name, predict_field, forecast_range)
    job_id = request["job_id"]
    st.query_params.from_dict({
        "job_id": job_id,
        "predict_field": predict_field,
        "device_id": device_id,
        "device_name": device_name,
        "device_type": device_type,
        "forecast_range": forecast_range
    })

@st.cache_data
def get_forecast_data_cache(*arg):
    return get_forecast_data(*arg)

if 'job_id' in st.query_params:
    job_id = st.query_params.job_id
    with st.spinner('Waiting for forecasting result...'):
        predict_data = get_forecast_data_cache(job_id)
        st.session_state.predict_data = predict_data
        if predict_data["predict_data"] == None:
            get_forecast_data_cache.clear()


### RENDER page
if  st.session_state.predict_data:
    predict_data= st.session_state.predict_data

    job_status = predict_data['status']
    if job_status == "Success":
        st.success('Forecast completed!')
    else:
        st.warning("Forecasting is in-progress, please wait")

    job_metadata = predict_data["job_metadata"]
    
    st.markdown(f'## {job_metadata["device_type"]}: {job_metadata["device_name"]}')
    
    if predict_data["predict_data"]:
        # Extract actual data and forecast data
        data = predict_data["predict_data"]['data']
        forecast_data = predict_data["predict_data"]['forecast']

        # Convert both data and forecast_data into DataFrames
        data = pd.DataFrame(data)
        forecast_data = pd.DataFrame(forecast_data)

        # Convert 'ts' to datetime for both
        data['datetime'] = pd.to_datetime(data['ts'])
        forecast_data['datetime'] = pd.to_datetime(forecast_data['ts'])

        last_row = data.iloc[[-1]]
        forecast_data = pd.concat([last_row, forecast_data], ignore_index=True)

        # Create the figure
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=data['datetime'],
            y=data[predict_field],
            mode='lines',
            name=predict_field,
            line=dict(color="#00897b", dash='solid')
        ))

        fig.add_trace(go.Scatter(
            x=forecast_data['datetime'],
            y=forecast_data[predict_field],
            mode='lines',
            name=f'Forecast {predict_field}',
            line=dict(color='#ADD8E6', dash='dash')
        ))

        # Update layout
        fig.update_layout(height=500, title=f"Forecast Data in {job_metadata['forecast_range']}")

        # Display the figure in Streamlit
        st.plotly_chart(fig)
else:
    st.markdown('Please select Forecast parameters and press Update')