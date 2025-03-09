import streamlit as st
import requests
import st_local_storage
import time
from routes import get_url, RouteName
from utils.i18n import get_text

st_ls = st_local_storage.StLocalStorage()

token = st_ls.get('token', cached=False)

refreshToken = st_ls.get('refreshToken', cached=False)

if token and refreshToken:
    st.switch_page("Homepage.py")

def authenticate(username, password):
    url = get_url(RouteName.POST_LOGIN)
    payload = {"username": username, "password": password}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(get_text("login.failed"))
        return None

def login_page():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.title(get_text("login.title"))
    
    # Create a login form
    with st.form("login_form"):
        username = st.text_input(get_text("login.username"))
        password = st.text_input(get_text("login.password"), type="password")
        submit = st.form_submit_button(get_text("login.loginButton"))
    token = None
    refreshToken = None

    if submit:
        auth_response = authenticate(username, password)
        if auth_response is not None:
            token = auth_response['token']
            refreshToken = auth_response['refreshToken']
    if token and refreshToken:
        st_ls.set("token", token)
        st_ls.set("refreshToken", refreshToken)
        time.sleep(1)
        st.switch_page("Homepage.py")

login_page()
