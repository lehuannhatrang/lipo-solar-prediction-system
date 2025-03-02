from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy import func
from middlewares import require_authentication
from apis.weev import WeevRequest, WEEVRouteName, get_weev_url, extract_devices_info, get_timeseries_data
import logging

weev_request = WeevRequest()

class DeviceIdsResource(Resource):
    @swag_from("../swagger/device/ids/GET.yml")
    @require_authentication
    def get(self):
        try:
            device_type = request.args.get('device_type')
            include_customer = request.args.get('include_customer_entity')

            response = weev_request.get(get_weev_url(WEEVRouteName.GET_CUSTOMER_DEVICES, include_customer=include_customer))
            
            if response.status_code != 200:
                logging.error(f"WEEV API error: {response.text}")
                return {"message": "Error fetching devices from WEEV"}, response.status_code
            try:
                all_devices_response = response.json()
            except ValueError as e:
                logging.error(f"Invalid JSON response from WEEV API: {str(e)}")
                return {"message": "Invalid response from WEEV API"}, 500

            if device_type == 'LIION_BATTERY':
                lion_battery_devices = extract_devices_info(all_devices_response, 'LionBattery')
                return {'data': lion_battery_devices}, 200
                
            elif device_type == 'SOLAR_PANEL':
                solar_panel_devices = extract_devices_info(all_devices_response, 'SolarSystem')
                return {'data': solar_panel_devices}, 200
                
            else:
                return {"message": "Device type not found"}, 404
                
        except Exception as e:
            logging.error(f"Error in device IDs endpoint: {str(e)}")
            return {"message": "Internal server error"}, 500

class DeviceFieldsResource(Resource):
    @swag_from("../swagger/device/fields/GET.yml")
    @require_authentication
    def get(self):
        device_id = request.args.get('device_id')
        
        response = weev_request.get(get_weev_url(WEEVRouteName.GET_TIMESERIES_FIELDS, device_id=device_id))
        if response.status_code != 200:
            logging.error(f"WEEV API error: {response.text}")
            return {"message": "Error fetching timeseries fields from WEEV"}, response.status_code

        return {'device_data': response.json()}, 200
        
class DeviceDataResource(Resource):
    @swag_from("../swagger/device/data/GET.yml")
    @require_authentication
    def get(self, device_id):
        try:
            data_fields = request.args.getlist('data_fields')
            start_time = int(float(request.args.get('start_time')) *1000)
            end_time = int(float(request.args.get('end_time')) *1000)

            timeseries_data = get_timeseries_data(device_id, data_fields, start_time, end_time)

            return jsonify({'data': timeseries_data, 'device_id': device_id})
        except Exception as e:
            logging.error(f"Error in device data endpoint: {str(e)}")
            return {"message": "Internal server error"}, 500