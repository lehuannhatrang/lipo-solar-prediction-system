import streamlit as st
from authentication import AuthenRequest
from routes import VEEVRouteName, get_veev_url

def log_out_button():
    authen_request = AuthenRequest()
    st.markdown(
        """
        <style>
        .sidebar .bottom-button {
            position: absolute;
            bottom: 10px;
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with st.sidebar:
        
        @st.dialog("Are you sure you want to logout?")
        def confirm_logout():
            if st.button("Yes, log me out", type="primary"):
                authen_request.log_out()
                st.switch_page("pages/Login.py")
        if st.button('Logout', type="primary"):
            confirm_logout()