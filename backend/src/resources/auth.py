import jwt
import logging
from flask import request
from flask_restful import Resource
from flasgger import swag_from
from apis.weev.routes import get_weev_url, WEEVRouteName
from apis.weev.request import WeevRequest
import requests
from models.user_license import UserLicense

class LoginResource(Resource):
    @swag_from("../swagger/auth/login/POST.yml")
    def post(self):
        try:
            # Get username and password from request
            data = request.get_json()
            if not data or 'username' not in data or 'password' not in data:
                return {"message": "Username and password are required"}, 400

            username = data['username']
            password = data['password']

            # Call WEEV login endpoint
            login_url = get_weev_url(WEEVRouteName.POST_LOGIN)
            if not login_url:
                return {"message": "Could not resolve login URL"}, 500

            response = requests.post(
                login_url,
                json={
                    "username": username,
                    "password": password
                }
            )

            # Extract tokens from response
            weev_response = response.json()
            if not weev_response.get('token'):
                return {"message": "Invalid credentials"}, 401

            # Decode token to get email
            token = weev_response['token']
            try:
                decoded = jwt.decode(token, options={"verify_signature": False})
                email = decoded.get('sub')  # email is in 'sub' claim
                if not email:
                    return {"message": "Invalid token format"}, 401
            except Exception as e:
                logging.error(f"Error decoding token: {str(e)}")
                return {"message": "Invalid token format"}, 401

            # Check user license
            user_license = UserLicense.get_by_email(email)
            if not user_license:
                return {"message": "No license found for this email"}, 403

            if not user_license.is_valid():
                return {"message": "License is inactive or expired"}, 403

            # Update last login time
            user_license.update_last_login()

            # Return tokens to client
            return {
                "token": weev_response['token'],
                "refreshToken": weev_response.get('refreshToken')
            }, 200

        except Exception as e:
            logging.error(f"Login error: {str(e)}")
            return {"message": "Internal server error"}, 500
