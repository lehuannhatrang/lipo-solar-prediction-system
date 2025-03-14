from typing import Any, Dict, Optional
import streamlit as st
import requests
from routes import WEEVRouteName, get_weev_url
from st_local_storage import StLocalStorage
from datetime import datetime
import jwt
import time

def check_authenticate():
    if 'st_ls' not in globals():
        st_ls = StLocalStorage()
    token = st_ls.get('token')
    refreshToken = st_ls.get('refreshToken')
    if (not token) or (not refreshToken):
        st.switch_page("pages/Login.py")
    return True

class AuthenRequest:
    is_renewing_token = False
    def __init__(self):
        """
        Initialize the AuthenRequest class.

        :param local_storage_handler: An object with a `get` method to fetch the token.
        """
        self.local_storage_handler = StLocalStorage()

    def _get_auth_header(self) -> Dict[str, str]:
        """
        Get the Authorization header with the token from local storage.

        :return: A dictionary with the Authorization header.
        """
        token = self.local_storage_handler.get('token')
        if not token:
            st.error("Token not found in local storage. Please log in.")
            raise ValueError("Token is missing")
        
        jwt_decode = jwt.decode(token, options={"verify_signature": False})
        expire_timestamp = jwt_decode['exp'] 
        current_timestamp = datetime.now().timestamp()
        if expire_timestamp < current_timestamp:
            if self.is_renewing_token:
                time.sleep(1)
            else:
                self.is_renewing_token = True
                try:
                    self.renew_token()
                    self.is_renewing_token = False
                except Exception as e:
                    self.is_renewing_token = False
            token = self.local_storage_handler.get('token', cached=False)
        
        return {"x-authorization": f"Bearer {token}"}

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        headers = kwargs.get("headers", {})
        headers.update(self._get_auth_header())
        kwargs["headers"] = headers
        response = requests.request(method, url, **kwargs)
        if response.status_code == 401:
            self.log_out()
            st.switch_page("pages/Login.py")
        return response

    def get(self, url: str, **kwargs) -> requests.Response:
        return self.request("GET", url, **kwargs)

    def post(self, url: str, data: Optional[Any] = None, json: Optional[Any] = None, **kwargs) -> requests.Response:
        return self.request("POST", url, data=data, json=json, **kwargs)

    def put(self, url: str, data: Optional[Any] = None, **kwargs) -> requests.Response:
        return self.request("PUT", url, data=data, **kwargs)

    def delete(self, url: str, **kwargs) -> requests.Response:
        return self.request("DELETE", url, **kwargs)

    def patch(self, url: str, data: Optional[Any] = None, **kwargs) -> requests.Response:
        return self.request("PATCH", url, data=data, **kwargs)
    
    def renew_token(self):
        try:
            refresh_token = self.local_storage_handler.get('refreshToken')
            request_body = {
                "refreshToken": refresh_token
            }
            response = requests.request('POST', get_weev_url(WEEVRouteName.POST_RENEW_TOKEN), json=request_body)
            response_val = response.json()
            if "token" in response_val and "refreshToken" in response_val:
                self.local_storage_handler.set("token", response_val['token'])
                self.local_storage_handler.set("refreshToken", response_val['refreshToken'])
        except Exception as e:
            self.local_storage_handler.delete('token')
            self.local_storage_handler.delete('refreshToken')

    def get_user_info(self, cached=True):
        if cached and 'user_info' in st.session_state:
            return st.session_state['user_info']
        token = self.local_storage_handler.get('token')
        jwt_decode = jwt.decode(token, options={"verify_signature": False})
        user_id = jwt_decode['userId']
        response = self.request('GET', get_weev_url(WEEVRouteName.GET_USER_INFO, user_id=user_id))
        user_info = response.json()
        st.session_state['user_info'] = user_info
        return user_info

    def log_out(self):
        response = self.request('POST',get_weev_url(WEEVRouteName.POST_LOG_OUT))
        self.local_storage_handler.delete('token')
        self.local_storage_handler.delete('refreshToken')
        time.sleep(0.5)