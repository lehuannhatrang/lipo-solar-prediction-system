from datetime import datetime
from flasgger import swag_from
from flask import request
from flask_restful import Resource
from models import PredictionJob
from celery_init import forecast_async
from celery.result import AsyncResult
from middlewares import require_authentication
from apis.weev import get_timeseries_data
import json
from datetime import datetime
import math

class ForecastResource(Resource):
    @swag_from("../swagger/forecast/GET.yml")
    @require_authentication
    def get(self, job_id):
        job = PredictionJob.query.filter_by(job_id=job_id).first()
        if job:
            result = AsyncResult(job_id)
            job.predict_data = None
            if job.status != 'Success':
                if result.ready():
                    job.predict_data = result.result
                    job.status = 'Success'
                    job.save()
            
            return {
                "job_id": str(job.job_id),
                "created_by": str(job.created_by),
                "created_ts": job.created_ts.isoformat(),
                "updated_ts": job.updated_ts.isoformat(),
                "type": job.type,
                "status": job.status,
                "result_url": job.result_url,
                "job_metadata": job.job_metadata,
                "predict_data": job.predict_data
            }
        else:
            return {"message": "Job not found"}, 404
        
    @require_authentication
    @swag_from("../swagger/forecast-request/POST.yml")
    def post(self):
        try:
            data = request.get_json()
            
            data_fields = [data['predict_field']]
            end_time = math.floor(datetime.now().timestamp() * 1000)
            start_time = end_time - (28 * 24 * 3600 * 1000)

            timeseries_data = get_timeseries_data(data['device_id'], data_fields, start_time, end_time)
            if not timeseries_data or len(timeseries_data) == 0:
                return {"message": "No data found for prediction"}, 400
            
            job = forecast_async.apply_async(args=[data['predict_field'], timeseries_data])
            job_id = job.id
            created_ts = datetime.now()
            new_job = PredictionJob(
                job_id=job_id,
                created_by="d15888d1-ddc5-4feb-9165-0c2383bde1a0",
                created_ts=created_ts,
                updated_ts=created_ts,
                type="forecast",
                status="Pending",
                result_url=None,
                job_metadata=data
            )
            new_job.save()
            return {
                "message": "Prediction job created successfully",
                "job_id": job_id,
                "created_by": str(new_job.created_by),
                "created_ts": new_job.created_ts.isoformat(),
                "updated_ts": new_job.updated_ts.isoformat(),
                "type": new_job.type,
                "status": new_job.status,
                "job_metadata": data
            }, 201
        except Exception as e:
            print('ERROR')
            print(e)
            return {"message": "Internal Error"}, 500
        
        
class RULPredictionResource(Resource):
    @swag_from("../swagger/rul-prediction/GET.yml")
    @require_authentication
    def get(self, job_id):
        try:
            job = PredictionJob.query.filter_by(job_id=job_id).first()
            if job:
                result = AsyncResult(job_id)
                print(result.result)
                if job.status != 'Success':
                    if result.ready():
                        job.predict_data = result.result
                        job.status = 'Success'
                        job.save()
                
                return {
                    "job_id": str(job.job_id),
                    "created_by": str(job.created_by),
                    "created_ts": job.created_ts.isoformat(),
                    "updated_ts": job.updated_ts.isoformat(),
                    "type": job.type,
                    "status": job.status,
                    "result_url": job.result_url,
                    "job_metadata": job.job_metadata,
                    "predict_data": job.predict_data
                }
            else:
                return {"message": "Job not found"}, 404
        except Exception as e:
            print('ERROR')
            print(e)
            return {"message": "Internal Error"}, 500
    
    @require_authentication
    @swag_from("../swagger/rul-prediction/POST.yml")
    def post(self):
        try:
            data = request.get_json()
            
            # Get historical data for RUL prediction
            data_fields = ['solar_battery_voltage', 'solar_battery_current', 'solar_battery_temperature']  # Required fields for RUL prediction
            end_time = math.floor(datetime.now().timestamp() * 1000)
            start_time = end_time - (30 * 24 * 3600 * 1000)  # Last 30 days of data

            timeseries_data = get_timeseries_data(data['device_id'], data_fields, start_time, end_time)
            if not timeseries_data or len(timeseries_data) == 0:
                return {"message": "No data found for RUL prediction"}, 400
            
            # Start async RUL prediction task
            from celery_init import rul_async  # Import here to avoid circular dependency
            job = rul_async.apply_async(args=[timeseries_data])
            job_id = job.id
            created_ts = datetime.now()
            
            # Create and save prediction job
            new_job = PredictionJob(
                job_id=job_id,
                created_by=data.get('user_id', "d15888d1-ddc5-4feb-9165-0c2383bde1a0"),
                created_ts=created_ts,
                updated_ts=created_ts,
                type="rul_prediction",
                status="Pending",
                result_url=None,
                job_metadata={
                    "device_id": data['device_id'],
                    "data_fields": data_fields,
                    "start_time": start_time,
                    "end_time": end_time
                }
            )
            new_job.save()
            
            return {
                "message": "RUL prediction job created successfully",
                "job_id": job_id,
                "created_by": str(new_job.created_by),
                "created_ts": new_job.created_ts.isoformat(),
                "updated_ts": new_job.updated_ts.isoformat(),
                "type": new_job.type,
                "status": new_job.status,
                "job_metadata": new_job.job_metadata
            }, 201
            
        except Exception as e:
            print('ERROR')
            print(e)
            return {"message": "Internal Error"}, 500
