from flask_restful import Api
from flask import Blueprint
from resources import LoginResource

# Initialize Blueprint for routes
AUTH_BLUEPRINT = Blueprint('auth_api', __name__)

# Initialize API and add resources
Api(AUTH_BLUEPRINT).add_resource(LoginResource, '/auth/login', endpoint='auth_login')