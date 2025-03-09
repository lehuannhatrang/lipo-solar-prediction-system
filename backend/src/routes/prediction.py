from flask_restful import Api
from flask import Blueprint
from resources import RULPredictionResource

# Initialize Blueprint for routes
PREDICTION_BLUEPRINT = Blueprint('prediction_api', __name__)

# Initialize API and add resources
Api(PREDICTION_BLUEPRINT).add_resource(RULPredictionResource, '/prediction/rul', endpoint='rul_prediction_create')
Api(PREDICTION_BLUEPRINT).add_resource(RULPredictionResource, '/prediction/rul/<job_id>', endpoint='rul_prediction_detail')
