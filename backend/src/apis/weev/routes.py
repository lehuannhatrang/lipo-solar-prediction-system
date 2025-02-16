from enum import Enum
import os

WEEV_URL = os.getenv('WEEV_URL', 'https://prod.weev.vn')
    
class WEEVRouteName(Enum):
    GET_USER_INFO = 'GET_USER_INFO'
    GET_CUSTOMER_DEVICES = 'GET_CUSTOMER_DEVICES'
    POST_RENEW_TOKEN = 'POST_RENEW_TOKEN'
    POST_LOG_OUT = 'POST_LOG_OUT'
    POST_LOGIN = 'POST_LOGIN'

WEEV_ROUTES = {
    "GET_USER_INFO": '/user/{user_id}',
    "GET_CUSTOMER_DEVICES": '/deviceInfos/all?pageSize=100&page=0',
    "POST_RENEW_TOKEN": '/auth/token',
    "POST_LOG_OUT": '/auth/logout',
    "POST_LOGIN": '/auth/login'
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