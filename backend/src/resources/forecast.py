import uuid
from datetime import datetime
from flask import request, jsonify
from flask_restful import Resource
from models import PredictionJob

class ForecastResource(Resource):
    def get(self, jobId):
        job = PredictionJob.query.filter_by(job_id=jobId).first()

        if job:
            return {
                "job_id": str(job.job_id),
                "created_by": str(job.created_by),
                "created_ts": job.created_ts.isoformat(),
                "updated_ts": job.updated_ts.isoformat(),
                "type": job.type,
                "status": job.status,
                "result_url": job.result_url
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
                result_url=None
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
            }, 201
        except Exception as e:
            print('ERROR')
            print(e)
            return {"message": "Internal Error"}, 500
        