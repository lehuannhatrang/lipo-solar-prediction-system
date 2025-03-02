import streamlit as st
from authentication import AuthenRequest
from components.logout_button.index import log_out_button

def user_profile():
    authen_request = AuthenRequest()
    user_info = authen_request.get_user_info()

    # Add the profile icon with a placeholder
    if 'email' in user_info:
        st.markdown(
            f"""
            <div class="profile-icon-container">
                <img 
                    src="https://loremflickr.com/200/200" 
                    style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;"
                    alt="User Profile" 
                    title="User Profile"
                />
                <div class="dropdown-menu">
                    <div class="dropdown-item"><b>Name:</b>{user_info['name']}</div>
                    <div class="dropdown-item"><b>Email:</b>{user_info['email']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )