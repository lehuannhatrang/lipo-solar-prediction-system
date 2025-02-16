import os
import jwt
import logging
import requests
import redis
from functools import wraps
from flask import request, current_app
from apis.weev.routes import get_weev_url, WEEVRouteName
from models.user_license import UserLicense

# Initialize Redis connection
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0,
    decode_responses=True
)

TOKEN_CACHE_TTL = 3600  # 1 hour in seconds

class AuthMiddleware:
    @staticmethod
    def extract_user_info_from_token(token):
        try:
            # Decode JWT without verification to extract user info
            decoded = jwt.decode(token, options={"verify_signature": False})
            return decoded.get('userId'), decoded.get('customerId'), decoded.get('sub')
        except Exception as e:
            logging.error(f"Error extracting user info from token: {str(e)}")
            return None, None, None

    @staticmethod
    def check_token_cache(token):
        try:
            user_info = redis_client.get(f"auth_token:{token}")
            if user_info:
                return True
            return False
        except Exception as e:
            logging.error(f"Error checking token cache: {str(e)}")
            return False

    @staticmethod
    def cache_token(token, user_id, customer_id, email):
        try:
            redis_client.setex(
                f"auth_token:{token}",
                TOKEN_CACHE_TTL,
                f'{user_id},{customer_id},{email}'
            )
        except Exception as e:
            logging.error(f"Error caching token: {str(e)}")

    def verify_with_weev(self, token, user_id, customer_id, email):
        try:
            # First check user license
            user_license = UserLicense.get_by_email(email)
            if not user_license:
                logging.warning(f"No license found for email: {email}")
                return False

            if not user_license.is_valid():
                logging.warning(f"Invalid or expired license for email: {email}")
                return False

            # Get WEEV user info endpoint URL
            url = get_weev_url(WEEVRouteName.GET_USER_INFO, user_id=user_id)
            if not url:
                return False

            # Call WEEV API to verify user
            headers = {'X-Authorization': f'Bearer {token}'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                # Update last login time
                user_license.update_last_login()
                # Cache the valid token
                self.cache_token(token, user_id, customer_id, email)
                return True

            return False
        except Exception as e:
            logging.error(f"Error verifying with WEEV: {str(e)}")
            return False

    def authenticate(self):
        auth_token = request.headers.get('X-Authorization')
        if not auth_token:
            logging.warning("No authentication token provided")
            return {"message": "Authentication token is required"}, 401

        auth_token = auth_token.replace("Bearer ", "")

        # First check if token is in cache
        if self.check_token_cache(auth_token):
            # Token is valid and cached
            user_id, customer_id, email = redis_client.get(f"auth_token:{auth_token}").split(',')
            request.user_id = user_id
            request.customer_id = customer_id
            request.user_email = email
            return None

        # If not in cache, verify with WEEV
        user_id, customer_id, email = self.extract_user_info_from_token(auth_token)
        if not user_id or not email:
            return {"message": "Invalid token format"}, 401

        if not self.verify_with_weev(auth_token, user_id, customer_id, email):
            return {"message": "Unauthorized"}, 401

        # Store user info in request context
        request.user_id = user_id
        request.customer_id = customer_id
        request.user_email = email
        
        return None


def require_authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_result = AuthMiddleware().authenticate()
        if auth_result is not None:
            return auth_result
        return func(*args, **kwargs)
    return wrapper