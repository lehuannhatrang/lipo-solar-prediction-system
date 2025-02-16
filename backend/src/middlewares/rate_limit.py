import time
from functools import wraps
from flask import request, current_app
from collections import defaultdict
import logging

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.max_requests = 100  # Maximum requests per window
        self.window = 60  # Time window in seconds

    def is_rate_limited(self, key):
        now = time.time()
        
        # Remove old requests outside the window
        self.requests[key] = [req_time for req_time in self.requests[key] 
                            if now - req_time < self.window]
        
        # Check if the number of requests exceeds the limit
        if len(self.requests[key]) >= self.max_requests:
            return True
            
        # Add current request
        self.requests[key].append(now)
        return False

rate_limiter = RateLimiter()

def rate_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Use IP address as the rate limiting key
        key = request.remote_addr
        
        if rate_limiter.is_rate_limited(key):
            logging.warning(f"Rate limit exceeded for IP: {key}")
            return {"message": "Rate limit exceeded. Please try again later."}, 429
            
        return func(*args, **kwargs)
    return wrapper
