from flask_restful import Api
from flask import Blueprint
from resources.user_license import UserLicenseResource, UserLicenseListResource

# Initialize Blueprint for routes
USER_LICENSE_BLUEPRINT = Blueprint('user_license_api', __name__)

# Initialize API and add resources
api = Api(USER_LICENSE_BLUEPRINT)
api.add_resource(UserLicenseResource, '/user-license/<string:email>', endpoint='user_license')
api.add_resource(UserLicenseListResource, '/user-license', endpoint='user_license_list')
