from enum import Enum
import os

BACKEND_URI = os.getenv('BACKEND_URI', 'http://localhost:5000')

API_VERSION=os.getenv('API_VERSION', 'v1')

VEEV_URL = os.getenv('VEEV_URL', 'https://prod.weev.vn')

base_url = f'{BACKEND_URI}/api/{API_VERSION}'

class RouteName(Enum):
    GET_ALL_BATTERY_ID = 'GET_ALL_BATTERY_ID'
    GET_DEVICE_FIELDS = 'GET_DEVICE_FIELDS'
    GET_DEVICE_DATA = 'GET_DEVICE_DATA'
    GET_FORECAST = 'GET_FORECAST'
    POST_REQUEST_FORECAST = 'POST_REQUEST_FORECAST'

ROUTES = {
    "GET_ALL_BATTERY_ID": '/devices/all-ids',
    'GET_DEVICE_FIELDS': '/devices/fields',
    'GET_DEVICE_DATA': '/device/{device_id}',
    'GET_FORECAST': '/forecast/{job_id}',
    'POST_REQUEST_FORECAST': '/forecast-request'
}

def get_url(route_name, **kwargs):
    try:
        route = ROUTES[route_name.value].format(**kwargs)
        return f'{base_url}{route}'
    except Exception as e:
        print('Could not resolve route')
        print(e)
        return None
    

class VEEVRouteName(Enum):
    GET_USER_INFO = 'GET_USER_INFO'

VEEV_ROUTES = {
    "GET_USER_INFO": '/user/{user_id}',
}

veev_base_url = f'{VEEV_URL}/api'

def get_veev_url(route_name, **kwargs):
    try:
        route = VEEV_ROUTES[route_name.value].format(**kwargs)
        return f'{veev_base_url}{route}'
    except Exception as e:
        print('Could not resolve route')
        print(e)
        return None