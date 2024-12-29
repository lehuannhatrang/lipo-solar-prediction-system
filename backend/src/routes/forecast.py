from flask_restful import Api
from flask import Blueprint
from resources import ForecastResource, DemoForecastResource

# Initialize Blueprint for routes
FORECAST_BLUEPRINT = Blueprint('forecast_api', __name__)

# Initialize API and add resources
Api(FORECAST_BLUEPRINT).add_resource(ForecastResource, '/forecast-request', endpoint='forecast_create')
Api(FORECAST_BLUEPRINT).add_resource(ForecastResource, '/forecast/<job_id>', endpoint='forecast_detail')
Api(FORECAST_BLUEPRINT).add_resource(DemoForecastResource, '/get-demo-predict-data/<job_id>', endpoint='get_demo_data')
