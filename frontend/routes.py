from enum import Enum
import os

BACKEND_URI = os.getenv('BACKEND_URI', 'http://localhost:5000')

API_VERSION=os.getenv('API_VERSION', 'v1')

WEEV_URL = os.getenv('WEEV_URL', 'https://prod.weev.vn')

base_url = f'{BACKEND_URI}/api/{API_VERSION}'

class RouteName(Enum):
    GET_ALL_BATTERY_ID = 'GET_ALL_BATTERY_ID'
    GET_DEVICE_FIELDS = 'GET_DEVICE_FIELDS'
    GET_DEVICE_DATA = 'GET_DEVICE_DATA'
    GET_FORECAST = 'GET_FORECAST'
    GET_RUL_PREDICTION = 'GET_RUL_PREDICTION'
    POST_REQUEST_FORECAST = 'POST_REQUEST_FORECAST'
    POST_LOGIN = 'POST_LOGIN'
    GET_USER_LICENSES = 'GET_USER_LICENSES'
    GET_USER_LICENSE = 'GET_USER_LICENSE'
    PUT_USER_LICENSE = 'PUT_USER_LICENSE'
    POST_USER_LICENSE = 'POST_USER_LICENSE'
    POST_RUL_PREDICTION = 'POST_RUL_PREDICTION'

ROUTES = {
    "GET_ALL_BATTERY_ID": '/devices/all-ids',
    'GET_DEVICE_FIELDS': '/devices/fields',
    'GET_DEVICE_DATA': '/device/{device_id}',
    'GET_FORECAST': '/forecast/{job_id}',
    'GET_RUL_PREDICTION': '/prediction/rul/{job_id}',
    'POST_REQUEST_FORECAST': '/forecast-request',
    'POST_LOGIN': '/auth/login',
    'GET_USER_LICENSES': '/user-license',
    'GET_USER_LICENSE': '/user-license/{email}',
    'PUT_USER_LICENSE': '/user-license/{email}',
    'POST_USER_LICENSE': '/user-license',
    'POST_RUL_PREDICTION': '/prediction/rul'
}

def get_url(route_name, **kwargs):
    try:
        route = ROUTES[route_name.value].format(**kwargs)
        return f'{base_url}{route}'
    except Exception as e:
        print('Could not resolve route')
        print(e)
        return None
    

class WEEVRouteName(Enum):
    GET_USER_INFO = 'GET_USER_INFO'
    POST_RENEW_TOKEN = 'POST_RENEW_TOKEN'
    POST_LOG_OUT = 'POST_LOG_OUT'

WEEV_ROUTES = {
    "GET_USER_INFO": '/user/{user_id}',
    "POST_RENEW_TOKEN": '/auth/token',
    "POST_LOG_OUT": '/auth/logout'
}

weev_base_url = f'{WEEV_URL}/api'

def get_weev_url(route_name, **kwargs):
    try:
        route = WEEV_ROUTES[route_name.value].format(**kwargs)
        return f'{weev_base_url}{route}'
    except Exception as e:
        print('Could not resolve route')
        print(e)
        return None