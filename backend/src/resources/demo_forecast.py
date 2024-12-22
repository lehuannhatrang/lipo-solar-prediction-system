import uuid
from datetime import datetime, timedelta
from flask import request, jsonify
from flask_restful import Resource
from models import PredictionJob, LiionBatteryStatus
from config import FORECAST_RANGE

class DemoForecastResource(Resource):
    def get(self, job_id):
        job = PredictionJob.query.filter_by(job_id=job_id).first()

        if job:
            job_metadata = job.job_metadata
            device_id = job_metadata["device_id"]
            predict_field = job_metadata['predict_field']
            forecast_range = job_metadata["forecast_range"]
            forecast_days = FORECAST_RANGE[forecast_range]

            query = LiionBatteryStatus.query.filter_by(battery_id=device_id)
            
            query_all = query.all()

            device_data = [device.to_dict([predict_field, 'ts']) for device in query_all]
            sorted_device_data = sorted(device_data, key=lambda x: x['ts'])

            forecast_data = []
            for i in range(1, forecast_days*4):
                new_predict_ts = datetime.now() + i * timedelta(hours=6)
                predict_point = {
                    'ts': new_predict_ts.isoformat()
                }
                predict_point[predict_field] = sorted_device_data[-i if i < len(sorted_device_data) else -len(sorted_device_data) ][predict_field]
                forecast_data.append(predict_point)
            
            return jsonify({'data': sorted_device_data, 'forecast': forecast_data})
        else:
            return {"message": "Job not found"}, 404
        