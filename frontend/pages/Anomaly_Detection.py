import streamlit as st
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

import pandas as pd
from authentication import check_authenticate
from components.user_profile.index import user_profile
from utils import get_all_device_ids, create_year_heatmap, get_forecast_data, render_sidebar_navigation
from constants import device_type_labels, device_checkbox_labels, forecast_predict_fields, forecast_labels
import calendar
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
import plotly.graph_objects as go


check_authenticate()

render_sidebar_navigation()

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

user_profile()

st.sidebar.header('Anomaly Detection')

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
        st.sidebar.markdown(f'Device ID: {device_id[0]}')

# TIME RANGE SELECTION
current_time = datetime.now()
default_start_time = current_time - timedelta(days=90)
date_range = st.sidebar.date_input(
    "From - To",
    (default_start_time, current_time),
    None,
    current_time,
    format="MM.DD.YYYY",
)

def allow_submit():
    return bool(device_id)

if st.sidebar.button("Update",  type="primary", disabled=not allow_submit()):
    pass

@st.cache_data
def get_forecast_data_cache(*arg):
    return get_forecast_data(*arg)

if 'job_id' in st.query_params:
    job_id = st.query_params.job_id
    with st.spinner('Waiting for Anomaly result...'):
        predict_data = get_forecast_data_cache(job_id)
        st.session_state.predict_data = predict_data
        if predict_data["predict_data"] == None:
            get_forecast_data_cache.clear()

### HARDCODE DATA

def generate_anomaly_data(start_date, end_date):
    date_range = pd.date_range(start_date, end_date)
    anomaly_scores = np.random.normal(loc=40, scale=30, size=len(date_range))
    anomaly_scores = np.clip(anomaly_scores, 0, 100)
    data = pd.DataFrame({
        'Date': date_range,
        'Anomaly Score': anomaly_scores
    })
    return data


st.title("Anomaly Score Heatmap")

if len(date_range) == 2 and date_range[0] and date_range[1]:
    start_date = date_range[0]
    end_date = date_range[1]

    anomaly_data = generate_anomaly_data(start_date, end_date)
    st.write(f"Anomaly data from {start_date} to {end_date}")

    year_matrix, week_start_dates, data = create_year_heatmap(anomaly_data, start_date, end_date)
    week_start_dates_str = [date.strftime('%Y-%m-%d') for date in week_start_dates]

    fig = px.imshow(year_matrix, labels={'color': 'Anomaly Score'}, 
                    x=week_start_dates_str,
                    y=list(calendar.day_name),
                    color_continuous_scale='Greens', origin='lower')

    st.plotly_chart(fig)


    fig_chart = go.Figure()
    fig_chart.add_trace(go.Scatter(x=data['Date'], y=data['Anomaly Score'], mode='lines+markers', name='Anomaly Score', line=dict(color='#00897b')))

    high_anomaly_dates = data[data['Anomaly Score'] > 60]

    for date in high_anomaly_dates['Date']:
        fig_chart.add_vrect(
            x0=date - timedelta(days=0.5), x1=date + timedelta(days=0.5), 
            fillcolor="red", opacity=0.3, line_width=0,
            annotation_position="top left",
            annotation_text=""
        )

    fig_chart.update_layout(
        title="Anomaly Score Over Time",
        xaxis_title="Date",
        yaxis_title="Anomaly Score",
        xaxis=dict(tickformat='%Y-%m-%d'),
        showlegend=False
    )

    st.plotly_chart(fig_chart)