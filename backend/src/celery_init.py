from celery import Celery, Task, shared_task
from flask import Flask
import time
import os
import requests

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", '6379')

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_app = Celery('celery_jobs.forecast')
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    celery_app.Task = FlaskTask
    app.extensions["celery"] = celery_app
    return celery_app

def create_app(app_name) -> Flask:
    app = Flask(app_name)
    app.config.from_mapping(
        CELERY=dict(
            broker_url=f"redis://{REDIS_HOST}:{REDIS_PORT}",
            result_backend=f"redis://{REDIS_HOST}:{REDIS_PORT}", 
            task_ignore_result=True,
        )
    )
    app.config.from_prefixed_env()
    celery_init_app(app)
    return app

flask_app = create_app('forecast')
celery_app = flask_app.extensions["celery"]

@shared_task(ignore_result=False)
def forecast_async() -> int:
    time.sleep(5)
    forecast_endpoint = f'http://localhost:5000/api/v1/get-demo-predict-data/{forecast_async.request.id}'
    predict_data = requests.get(forecast_endpoint).json()
    return predict_data