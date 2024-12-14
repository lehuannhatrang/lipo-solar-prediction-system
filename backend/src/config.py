import os 

API_VERSION = os.getenv('API_VERSION', 'v1')

DB_CONFIG = {
    "host":  os.getenv('DB_CONNECTION_HOST', 'localhost'),
    "port": os.getenv('DB_CONNECTION_PORT', '32432'),
    "username": os.getenv('DB_USERNAME', 'postgres'),
    "password": os.getenv('DB_PASSWORD', 'postgres'),
    'database': os.getenv('DB_DATABASE', 'prediction_core')
}
