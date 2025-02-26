import time
import streamlit as st
from authentication import AuthenRequest
from routes import RouteName, get_url
import pandas as pd
from datetime import timedelta
import numpy as np

auth_request = AuthenRequest()

def get_all_device_ids(device_type, include_customer_entity=True):
    params = {
        'device_type': device_type,
        'include_customer_entity': include_customer_entity
    }
    response = auth_request.get(get_url(RouteName.GET_ALL_BATTERY_ID), params=params)
    return response.json()['data']

def render_sidebar_navigation():
    st.sidebar.page_link('Homepage.py', label='Home')
    st.sidebar.page_link('pages/Collections.py', label='Collections')
    st.sidebar.page_link('pages/Forecast.py', label='Forecast')
    st.sidebar.page_link('pages/Anomaly_Detection.py', label='Anomally Detection')

def get_device_fields(device_id):
    params = {
        'device_id': device_id
    }
    response = auth_request.get(get_url(RouteName.GET_DEVICE_FIELDS), params=params)
    return response.json()['device_data']


def get_device_data(device_type, device_id, data_fields, start_time, end_time):
    params = {
        'device_type': device_type,
        'data_fields': data_fields,
        'start_time': start_time,
        'end_time': end_time
    }
    response = auth_request.get(get_url(RouteName.GET_DEVICE_DATA, device_id=device_id), params=params)
    return response.json()

def request_forecast(device_type, device_id, device_name, predict_field, forecast_range):
    body = {
        'device_type': device_type,
        'device_id': device_id,
        'device_name': device_name,
        'predict_field': predict_field,
        'forecast_range': forecast_range
    }
    response = auth_request.post(get_url(RouteName.POST_REQUEST_FORECAST), json=body)
    return response.json()

def get_forecast_data(job_id):
    for i in range(0, 12):
        response = auth_request.get(get_url(RouteName.GET_FORECAST, job_id=job_id)).json()
        if response["predict_data"]:
            break
        time.sleep(5)
    return response

def create_year_heatmap(data, start_date, end_date):
    # Convert input dates to datetime objects
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Add columns for year, month, day, and weekday
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['Day'] = data['Date'].dt.day
    data['Weekday'] = data['Date'].dt.weekday  # 0=Monday, 6=Sunday
    data['Week'] = data['Date'].dt.isocalendar().week  # Week number
    data['ISO_Year'] = data['Date'].dt.isocalendar().year  # ISO Year
    
    # Filter data to only include the selected time range
    data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

    # Generate a consistent week index across year boundaries
    min_iso_year = data['ISO_Year'].min()
    data['Week_Index'] = (data['ISO_Year'] - min_iso_year) * 53 + data['Week']
    
    # Calculate start and end week indices
    start_week_index = ((start_date.isocalendar().year - min_iso_year) * 53 +
                        start_date.isocalendar()[1])
    end_week_index = ((end_date.isocalendar().year - min_iso_year) * 53 +
                      end_date.isocalendar()[1])

    # Create a matrix for the year, where rows represent days of the week and columns represent weeks
    max_weeks = end_week_index - start_week_index + 1  # Range of weeks to include
    week_matrix = np.zeros((7, max_weeks))  # 7 rows (days of the week), max_weeks columns

    # Populate the matrix with anomaly scores
    for _, row in data.iterrows():
        week_of_year = row['Week_Index'] - start_week_index  # Adjust to 0-based index
        day_of_week = row['Weekday']  # 0=Monday, 6=Sunday
        week_matrix[day_of_week, week_of_year] = row['Anomaly Score']

    # Define the range of weeks that need to be displayed (only weeks within the selected range)
    weeks_in_range = list(range(start_week_index, end_week_index + 1))

    # Calculate the starting date of each week
    week_start_dates = [start_date + timedelta(weeks=week - weeks_in_range[0],
                                               days=-start_date.weekday()) for week in weeks_in_range]

    return week_matrix, week_start_dates, data