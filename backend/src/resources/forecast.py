import uuid
from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource
from models import PredictionJob
from config import APP_ENV

class ForecastResource(Resource):
    def get(self, job_id):
        job = PredictionJob.query.filter_by(job_id=job_id).first()

        if job:
            if (APP_ENV == 'dev'):
                if (datetime.now() - job.created_ts).seconds > 10:
                    job.status = 'Success'
                    job.result_url = f"http://backend:5000/api/v1/get-demo-predict-data/{job_id}"
            return {
                "job_id": str(job.job_id),
                "created_by": str(job.created_by),
                "created_ts": job.created_ts.isoformat(),
                "updated_ts": job.updated_ts.isoformat(),
                "type": job.type,
                "status": job.status,
                "result_url": job.result_url,
                "job_metadata": job.job_metadata,
                "predict_data": None
            }
        else:
            return {"message": "Job not found"}, 404
        
    def post(self):
        try:
            data = request.get_json()
            job_id = str(uuid.uuid4())
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
        