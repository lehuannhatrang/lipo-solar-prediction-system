from datetime import datetime
from flasgger import swag_from
from flask import request, jsonify
from flask_restful import Resource
from models import PredictionJob
from config import APP_ENV, BACKEND_HOST
from celery_init import forecast_async
from celery.result import AsyncResult

class ForecastResource(Resource):
    @swag_from("../swagger/forecast/GET.yml")
    def get(self, job_id):
        job = PredictionJob.query.filter_by(job_id=job_id).first()
        if job:
            result = AsyncResult(job_id)
            job.predict_data = None
            if job.status != 'Success':
                if result.ready():
                    print('result: ', result.result)
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
        
    @swag_from("../swagger/forecast-request/POST.yml")
    def post(self):
        try:
            data = request.get_json()
            job = forecast_async.apply_async(args=[data['predict_field']])
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
        