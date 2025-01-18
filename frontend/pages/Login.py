import streamlit as st
import requests
import st_local_storage
import time

st.set_page_config(layout='centered', initial_sidebar_state='collapsed')

st_ls = st_local_storage.StLocalStorage()

token = st_ls.get('token', cached=False)

refreshToken = st_ls.get('refreshToken', cached=False)

if token and refreshToken:
    st.switch_page("Homepage.py")

def authenticate(username, password):
    url = "https://prod.weev.vn/api/auth/login"
    payload = {"username": username, "password": password}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()  # Returns token and refreshToken
    except requests.exceptions.RequestException as e:
        st.error("Login failed")
        return None

def login_page():
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.title("Login")
    
    # Create a login form
    with st.form("login_form"):
        username = st.text_input("Username", "thanhadmin@test.com")
        password = st.text_input("Password", "123456",type="password")
        submit = st.form_submit_button("Log In")
    token = None
    refreshToken = None

    if submit:
        auth_response = authenticate(username, password)
        token = auth_response['token']
        refreshToken = auth_response['refreshToken']
    if token and refreshToken:
        st_ls.set("token", token)
        st_ls.set("refreshToken", refreshToken)
        time.sleep(1)
        if st_ls.get("token", cached=False):
            st.switch_page("Homepage.py")

login_page()
