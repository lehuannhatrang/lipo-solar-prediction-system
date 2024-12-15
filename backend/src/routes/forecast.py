from flask_restful import Api
from flask import Blueprint
from resources import ForecastResource

# Initialize Blueprint for routes
FORECAST_BLUEPRINT = Blueprint('forecast_api', __name__)

# Initialize API and add resources
Api(FORECAST_BLUEPRINT).add_resource(ForecastResource, '/forecast', endpoint='forecast_create')
Api(FORECAST_BLUEPRINT).add_resource(ForecastResource, '/forecast/<jobId>', endpoint='forecast_detail')
