import requests
import logging
from flask import request as flask_request

class WeevRequest:
    def __init__(self):
        self.session = requests.Session()
    
    def _get_auth_header(self):
        auth_token = flask_request.headers.get('X-Authorization')
        if not auth_token:
            logging.error("No X-Authorization header found in request")
            return None
            
        # Add Bearer prefix if not present
        if not auth_token.startswith('Bearer '):
            auth_token = f'Bearer {auth_token}'
            
        return {'X-Authorization': auth_token}
    
    def _make_request(self, method, url, **kwargs):
        headers = self._get_auth_header()
        if not headers:
            raise Exception("Authorization header is required")
            
        # Merge headers with any existing headers in kwargs
        if 'headers' in kwargs:
            kwargs['headers'].update(headers)
        else:
            kwargs['headers'] = headers
            
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Log request details for debugging
            logging.debug(f"Request URL: {url}")
            logging.debug(f"Request Headers: {kwargs.get('headers', {})}")
            logging.debug(f"Response Status: {response.status_code}")
            logging.debug(f"Response Headers: {response.headers}")
            
            if response.status_code != 200:
                logging.error(f"WEEV API error response: {response.text}")
                
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Error making request to WEEV API: {str(e)}")
            raise
    
    def get(self, url, **kwargs):
        return self._make_request('GET', url, **kwargs)
    
    def post(self, url, **kwargs):
        return self._make_request('POST', url, **kwargs)
    
    def put(self, url, **kwargs):
        return self._make_request('PUT', url, **kwargs)
    
    def delete(self, url, **kwargs):
        return self._make_request('DELETE', url, **kwargs)
    
    def patch(self, url, **kwargs):
        return self._make_request('PATCH', url, **kwargs)