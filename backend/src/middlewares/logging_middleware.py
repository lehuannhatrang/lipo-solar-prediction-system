import time
import logging
from functools import wraps
from flask import request, g

def setup_request_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def log_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Start timer
        start_time = time.time()
        
        # Store start time in Flask's g object
        g.start_time = start_time
        
        # Log request details
        logging.info(f"Request started: {request.method} {request.path}")
        logging.debug(f"Request headers: {dict(request.headers)}")
        
        # Execute the route function
        response = func(*args, **kwargs)
        
        # Calculate duration
        duration = time.time() - g.start_time
        
        # Log response details
        status_code = response.status_code if hasattr(response, 'status_code') else 200
        logging.info(f"Request completed: {request.method} {request.path} - Status: {status_code} - Duration: {duration:.2f}s")
        
        return response
    return wrapper
