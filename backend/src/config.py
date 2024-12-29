import os 

API_VERSION = os.getenv('API_VERSION', 'v1')

DB_CONFIG = {
    "host":  os.getenv('DB_CONNECTION_HOST', 'localhost'),
    "port": os.getenv('DB_CONNECTION_PORT', '32432'),
    "username": os.getenv('DB_USERNAME', 'postgres'),
    "password": os.getenv('DB_PASSWORD', 'postgres'),
    'database': os.getenv('DB_DATABASE', 'prediction_core')
}

APP_ENV = os.getenv('ENV', 'dev')
BACKEND_HOST = os.getenv('BACKEND_HOST', 'backend')

FORECAST_RANGE = {
    '5_DAYS': 5,
    '15_DAYS': 15,
    '30_DAYS': 30
}