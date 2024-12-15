from flask_restful import Api
from flask import Blueprint
from resources import DeviceIdsResource, DeviceDataResource, DeviceFieldsResource

# Initialize Blueprint for routes
DEVICE_BLUEPRINT = Blueprint('device_api', __name__)

# Initialize API and add resources
Api(DEVICE_BLUEPRINT).add_resource(DeviceIdsResource, '/devices/all-ids', endpoint='devices_all-ids')
Api(DEVICE_BLUEPRINT).add_resource(DeviceFieldsResource, '/devices/fields', endpoint='devices_fields')
Api(DEVICE_BLUEPRINT).add_resource(DeviceDataResource, '/device/<device_id>', endpoint='device_data')
