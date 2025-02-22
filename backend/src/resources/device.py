from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from models import LiionBatteryStatus, SolarPanelBatteryStatus
from sqlalchemy import func
from middlewares import require_authentication
from apis.weev import WeevRequest, WEEVRouteName, get_weev_url, extract_devices_info, extract_timeseries_data
import logging
from datetime import datetime

weev_request = WeevRequest()

class DeviceIdsResource(Resource):
    @swag_from("../swagger/device/ids/GET.yml")
    @require_authentication
    def get(self):
        try:
            device_type = request.args.get('device_type')
            
            # Get devices from WEEV API
            response = weev_request.get(get_weev_url(WEEVRouteName.GET_CUSTOMER_DEVICES))
            
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
        device_type = request.args.get('device_type')
        data_fields = request.args.getlist('data_fields')
        start_time = int(float(request.args.get('start_time')) *1000)
        end_time = int(float(request.args.get('end_time')) *1000)

        params = {
            'keys': data_fields,
            'startTs': start_time,
            'endTs': end_time,
            'intervalType': 'MILLISECONDS',
            'interval': 21600000,
            'agg': 'AVG',
            'orderBy': 'ASC',
            'useStrictDataTypes': 'true'
        }

        response = weev_request.get(get_weev_url(WEEVRouteName.GET_TIMESERIES_DATA, device_id=device_id), params=params)
        if response.status_code != 200:
            logging.error(f"WEEV API error: {response.text}")
            return {"message": "Error fetching timeseries data from WEEV"}, response.status_code
        response_data = response.json()
        # result_dict = {}
        # for key in data_fields:
        #     if key in response_data:
        #         field_data = [ {'timestamp': datetime.fromtimestamp(item['ts']/1000).isoformat(), key: item['value']} for item in response_data[key]]
        #         for item in field_data:
        #             if item['timestamp'] in result_dict:
        #                 result_dict[item['timestamp']].update({key: item[key]})
        #             else:
        #                 result_dict[item['timestamp']] = {key: item[key]}
        # result = [ {'timestamp': timestamp, **result_dict[timestamp]} for timestamp in result_dict.keys() ]

        result = extract_timeseries_data(response_data)

        return jsonify({'data': result, 'device_id': device_id})
        
        valid_fields = None
        if device_type == 'LIION_BATTERY':
            query = LiionBatteryStatus.query.filter_by(battery_id=device_id)

            query = query.filter(
                func.extract('epoch', LiionBatteryStatus.ts) >= start_time,
                func.extract('epoch', LiionBatteryStatus.ts) <= end_time
            )            
            if data_fields:
                valid_fields = [getattr(LiionBatteryStatus, field) for field in data_fields if hasattr(LiionBatteryStatus, field)]
                if not valid_fields:
                    return {'error': 'Invalid data_fields provided'}, 400
                
            # Execute the query
            query_all = query.all()
            device_data = [device.to_dict(data_fields + ['ts']) for device in query_all]
            return jsonify({'data': device_data, 'device_id': device_id})
            
        elif device_type == 'SOLAR_PANEL':
            query = SolarPanelBatteryStatus.query.filter_by(panel_id=device_id)

            query = query.filter(
                func.extract('epoch', SolarPanelBatteryStatus.ts) >= start_time,
                func.extract('epoch', SolarPanelBatteryStatus.ts) <= end_time
            )            
            if data_fields:
                valid_fields = [getattr(SolarPanelBatteryStatus, field) for field in data_fields if hasattr(SolarPanelBatteryStatus, field)]
                if not valid_fields:
                    return {'error': 'Invalid data_fields provided'}, 400
                
            # Execute the query
            query_all = query.all()
            device_data = [device.to_dict(data_fields + ['ts']) for device in query_all]
            return jsonify({'data': device_data, 'device_id': device_id})
        else:
            return {"message": "Device type not found"}, 404