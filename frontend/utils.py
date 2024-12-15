import requests
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