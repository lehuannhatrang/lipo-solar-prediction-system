from typing import Any, Dict, Optional
import streamlit as st
import requests
from routes import VEEVRouteName, get_veev_url
from st_local_storage import StLocalStorage
import jwt

def check_authenticate():
    if 'st_ls' not in globals():
        st_ls = StLocalStorage()
    token = st_ls.get('token')
    refreshToken = st_ls.get('refreshToken')
    if (not token) or (not refreshToken):
        st.switch_page("pages/Login.py")
    return True

class AuthenRequest:
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
        return {"x-authorization": f"Bearer {token}"}

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Make an HTTP request with the Authorization header included.

        :param method: HTTP method (GET, POST, etc.)
        :param url: The URL to send the request to.
        :param kwargs: Additional arguments passed to `requests.request`.
        :return: The Response object.
        """
        headers = kwargs.get("headers", {})
        # Merge Authorization header with any existing headers
        headers.update(self._get_auth_header())
        kwargs["headers"] = headers
        return requests.request(method, url, **kwargs)

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
    
    def get_user_info(self, cached=True):
        if cached and 'user_info' in st.session_state:
            return st.session_state['user_info']
        token = self.local_storage_handler.get('token')
        jwt_decode = jwt.decode(token, options={"verify_signature": False})
        user_id = jwt_decode['userId']
        response = self.request('GET', get_veev_url(VEEVRouteName.GET_USER_INFO, user_id=user_id))
        user_info = response.json()
        st.session_state['user_info'] = user_info
        return user_info
