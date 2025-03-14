from celery import Celery, Task, shared_task
from flask import Flask
import os
import boto3
import json
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import urllib3
import numpy as np
from datetime import datetime, timedelta

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", '6379')
BACKEND_HOST = os.getenv('BACKEND_HOST', 'localhost')

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
def forecast_async(predict_field: str, timeseries_data: list) -> int:
    input_size = 3
    sequence_length = 40
    # AWS credentials and configuration
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = 'ap-northeast-2'
    service = 'sagemaker-runtime'
    
    # Prepare the request
    endpoint_name = "soh-predictor-serverless"
    
    sagemaker_runtime = boto3.client(
        service_name=service, 
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region
    )
    

    # Send the request
    try:
        # input_data = np.random.rand(1, sequence_length, input_size).tolist()
        input_data = [[[data_point[predict_field], 0, 0] for data_point in timeseries_data[-sequence_length:]]]

        body = json.dumps({"features": input_data})
        
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            Body=body,
            Accept='application/json',
            ContentType='application/json'
        )
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]

        if status_code == 200:
            response_data = response["Body"].read().decode("utf-8")
            predictions_data = json.loads(response_data)['predictions'][0]

            forecast_data = [
                {'timestamp': (datetime.now() + i * timedelta(hours=6)).isoformat(), predict_field: predictions_data[i]*100 + 60} for i in range(len(predictions_data))
            ]

            result = {
                'data': timeseries_data,
                'forecast': forecast_data
            }
            return result
        else:
            raise Exception(f"Error calling SageMaker endpoint: {status_code} - {response}")
            
    except Exception as e:
        raise Exception(f"Failed to call SageMaker endpoint: {str(e)}")

# @celery_app.task(name="rul_async")
@shared_task(ignore_result=False)
def rul_async(timeseries_data: list):
    """Asynchronous task to predict RUL using SageMaker endpoint
    
    Args:
        timeseries_data (list): List of time series data points
        
    Returns:
        dict: Dictionary containing the prediction results
    """
    # Initialize the SageMaker runtime client
    endpoint_name = 'rul-predictor-serverless'
    region = os.environ.get('AWS_DEFAULT_REGION', 'ap-northeast-2')
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    
    sagemaker_runtime = boto3.client(
        'sagemaker-runtime',
        region_name=region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
    )
    
    # Send the request
    try:
        # Prepare input data
        input_data = np.random.rand(1, 10, 3).tolist()  # TODO: Replace with actual data processing
        
        body = json.dumps({"features": input_data})
        
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            Body=body,
            Accept='application/json',
            ContentType='application/json'
        )
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        
        if status_code == 200:
            response_data = response["Body"].read().decode("utf-8")
            predictions = json.loads(response_data)['predictions'][0]
            
            # Process predictions
            result = {
                'rul_prediction': predictions[0]*3600*24,  # Assuming single RUL value
                'timestamp': datetime.now().isoformat()
            }
            
            return result
        else:
            raise Exception(f"Error calling SageMaker endpoint: {status_code} - {response}")
            
    except Exception as e:
        raise Exception(f"Failed to call SageMaker endpoint: {str(e)}")

