import streamlit as st
from authentication import AuthenRequest

def log_out_button():
    authen_request = AuthenRequest()
        
    @st.dialog("Are you sure you want to logout?")
    def confirm_logout():
        if st.button("Yes, log me out", type="primary"):
            authen_request.log_out()
            st.switch_page("pages/Login.py")
    if st.button('Logout'):
        confirm_logout()