from enum import Enum
import os

BACKEND_URI = os.getenv('BACKEND_URI', 'http://localhost:5000')
API_VERSION=os.getenv('API_VERSION', 'v1')

base_url = f'{BACKEND_URI}/api/{API_VERSION}'

class RouteName(Enum):
    GET_ALL_BATTERY_ID = 'GET_ALL_BATTERY_ID'
    GET_DEVICE_FIELDS = 'GET_DEVICE_FIELDS'
    GET_DEVICE_DATA = 'GET_DEVICE_DATA'

ROUTES = {
    "GET_ALL_BATTERY_ID": '/devices/all-ids',
    'GET_DEVICE_FIELDS': '/devices/fields',
    'GET_DEVICE_DATA': '/device/{device_id}'
}

def get_url(route_name, **kwargs):
    try:
        route = ROUTES[route_name.value].format(**kwargs)
        print(route)
        return f'{base_url}{route}'
    except Exception as e:
        print('Could not resolve route')
        print(e)
        return None