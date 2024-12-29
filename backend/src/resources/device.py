from flasgger import swag_from
from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource
from models import LiionBatteryStatus, SolarPanelBatteryStatus
from sqlalchemy import func

class DeviceIdsResource(Resource):
    @swag_from("../swagger/device/ids/GET.yml")
    def get(self):
        device_type = request.args.get('device_type')
        if device_type == 'LIION_BATTERY':
            all_battery_ids = LiionBatteryStatus.query.with_entities(LiionBatteryStatus.battery_id).distinct().all()
            
            # Convert the result into a list of battery IDs
            unique_battery_ids = [battery_id[0] for battery_id in all_battery_ids]
            
            return {'device_ids': unique_battery_ids}, 200
        elif device_type == 'SOLAR_PANEL':
            all_panel_ids = SolarPanelBatteryStatus.query.with_entities(SolarPanelBatteryStatus.panel_id).distinct().all()
            
            # Convert the result into a list of battery IDs
            unique_panel_ids = [panel_id[0] for panel_id in all_panel_ids]
            
            return {'device_ids': unique_panel_ids}, 200
        else:
            return {"message": "Device type not found"}, 404
        

class DeviceFieldsResource(Resource):
    @swag_from("../swagger/device/fields/GET.yml")
    def get(self):
        device_type = request.args.get('device_type')
        
        if device_type == 'LIION_BATTERY':
            # Get all columns from the LiionBatteryStatus model
            all_columns = [column.name for column in LiionBatteryStatus.__table__.columns]
            
            return {'device_data': all_columns}, 200
        
        elif device_type == 'SOLAR_PANEL':
            # Get all columns from the LiionBatteryStatus model
            all_columns = [column.name for column in SolarPanelBatteryStatus.__table__.columns]
            
            return {'device_data': all_columns}, 200
        
        else:
            return {"message": "Device type not found"}, 404
        
class DeviceDataResource(Resource):
    @swag_from("../swagger/device/data/GET.yml")
    def get(self, device_id):
        device_type = request.args.get('device_type')
        data_fields = request.args.getlist('data_fields')
        start_time = float(request.args.get('start_time'))
        end_time = float(request.args.get('end_time'))

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