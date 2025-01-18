import streamlit as st
from authentication import AuthenRequest

def user_profile():
    user_info = AuthenRequest().get_user_info()

    # Add the profile icon with a placeholder
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