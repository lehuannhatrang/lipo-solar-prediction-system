import requests
import time
from routes import RouteName, get_url

def get_all_device_ids(device_type):
    params = {
        'device_type': device_type
    }
    response = requests.get(get_url(RouteName.GET_ALL_BATTERY_ID), params=params)
    return response.json()['device_ids']

def get_device_fields(device_type):
    params = {
        'device_type': device_type
    }
    response = requests.get(get_url(RouteName.GET_DEVICE_FIELDS), params=params)
    return response.json()['device_data']


def get_device_data(device_type, device_id, data_fields, start_time, end_time):
    params = {
        'device_type': device_type,
        'data_fields': data_fields,
        'start_time': start_time,
        'end_time': end_time
    }
    response = requests.get(get_url(RouteName.GET_DEVICE_DATA, device_id=device_id), params=params)
    return response.json()

def request_forecast(device_type, device_id, predict_field, forecast_range):
    body = {
        'device_type': device_type,
        'device_id': device_id,
        'predict_field': predict_field,
        'forecast_range': forecast_range
    }
    response = requests.post(get_url(RouteName.POST_REQUEST_FORECAST), json=body)
    return response.json()

def get_forecast_data(job_id):
    for i in range(0, 12):
        response = requests.get(get_url(RouteName.GET_FORECAST, job_id=job_id)).json()
        if response['result_url']:
            predict_data = requests.get(response['result_url']).json()
            response["predict_data"] = predict_data
            break
        time.sleep(5)
    return response