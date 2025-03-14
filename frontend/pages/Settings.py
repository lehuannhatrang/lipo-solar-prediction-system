import streamlit as st
from utils import set_page_config

# set_page_config()

from authentication import check_authenticate, AuthenRequest
from components.language_selector import language_selector
from utils import render_sidebar_navigation
from utils.i18n import get_text
from components.logout_button.index import log_out_button

authen_request = AuthenRequest()

check_authenticate()

# Render sidebar navigation
render_sidebar_navigation()

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Page title
st.title(get_text('settings.title')) 

st.header(get_text('settings.userInfo'))

# Get current user info
user = authen_request.get_user_info()

if user:
    st.markdown(f"**{get_text('settings.id')}:** {user['id']['id']}")
    st.markdown(f"**{get_text('settings.email')}:** {user['email']}")
    st.markdown(f"**{get_text('settings.phone')}:** {user['phone'] or '-'}")
else:
    st.warning(get_text('settings.userNotFound'))


# Create two columns for layout
col1, col2 = st.columns([1, 2])
with col1:
    st.header(get_text('settings.languageSettings'))
    language_selector()


log_out_button()

# Add custom CSS for better spacing and layout
st.markdown("""
    <style>
    .stSelectbox {
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)
