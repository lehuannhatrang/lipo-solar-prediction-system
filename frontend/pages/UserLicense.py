import streamlit as st
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

from datetime import datetime
import pandas as pd
from authentication import check_authenticate, AuthenRequest
from routes import RouteName, get_url
from utils import render_sidebar_navigation
from utils_i18n.i18n import get_text


# Check authentication
check_authenticate()

# Render sidebar navigation
render_sidebar_navigation()

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize authentication request
authen_request = AuthenRequest()

# Page title
st.title(get_text('userLicense.title'))

# Function to format datetime
def format_datetime(dt_str):
    if not dt_str:
        return "-"
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return dt_str

# Function to load user licenses
def load_user_licenses():
    try:
        response = authen_request.get(get_url(RouteName.GET_USER_LICENSES))
        if response.status_code == 200:
            return response.json()
        else:
            st.error(get_text('userLicense.loadError').format(error=response.text))
            return []
    except Exception as e:
        st.error(get_text('userLicense.loadError').format(error=str(e)))
        return []

# Function to update license status
def update_license_status(email, new_status):
    try:
        response = authen_request.put(
            get_url(RouteName.PUT_USER_LICENSE, email=email),
            json={"status": new_status}
        )
        if response.status_code == 200:
            st.success(get_text('userLicense.updateSuccess').format(email=email))
            return True
        else:
            st.error(get_text('userLicense.updateError').format(error=response.text))
            return False
    except Exception as e:
        st.error(get_text('userLicense.updateError').format(error=str(e)))
        return False

# Create new license section
with st.expander(get_text('userLicense.createNew'), expanded=False):
    with st.form("new_license_form"):
        new_email = st.text_input(get_text('userLicense.email'), key="new_email")
        new_user_id = st.text_input(f"{get_text('userLicense.userId')} ({get_text('userLicense.optional')})", key="new_user_id")
        new_status = st.selectbox(get_text('userLicense.status'), ["active", "inactive"], key="new_status")
        new_expired_ts = st.date_input(f"{get_text('userLicense.expirationDate')} ({get_text('userLicense.optional')})", value=None, key="new_expired_ts")
        
        submit_button = st.form_submit_button(get_text('userLicense.createButton'))
        
        if submit_button and new_email:
            try:
                data = {
                    "email": new_email,
                    "status": new_status
                }
                if new_user_id:
                    data["user_id"] = new_user_id
                if new_expired_ts:
                    data["expired_ts"] = new_expired_ts.isoformat()
                
                response = authen_request.post(
                    get_url(RouteName.POST_USER_LICENSE),
                    json=data
                )
                
                if response.status_code == 201:
                    st.success(get_text('userLicense.createSuccess').format(email=new_email))
                    st.rerun()
                else:
                    st.error(get_text('userLicense.createError').format(error=response.text))
            except Exception as e:
                st.error(get_text('userLicense.createError').format(error=str(e)))

# Load and display user licenses
licenses = load_user_licenses()

if licenses:
    # Convert to DataFrame for better display
    df = pd.DataFrame(licenses)
    
    # Reorder and rename columns
    columns = {
        'email': get_text('userLicense.email'),
        'user_id': get_text('userLicense.userId'),
        'status': get_text('userLicense.status'),
        'expired_ts': get_text('userLicense.expirationDate'),
        'last_login_ts': get_text('userLicense.lastLogin'),
        'created_at': get_text('userLicense.createdAt'),
        'updated_at': get_text('userLicense.updatedAt')
    }
    
    df = df.rename(columns=columns)
    
    # Format datetime columns
    datetime_cols = [
        get_text('userLicense.expirationDate'),
        get_text('userLicense.lastLogin'),
        get_text('userLicense.createdAt'),
        get_text('userLicense.updatedAt')
    ]
    for col in datetime_cols:
        if col in df.columns:
            df[col] = df[col].apply(format_datetime)

    # Configure column settings for the editor
    column_config = {
        get_text('userLicense.email'): st.column_config.TextColumn(
            get_text('userLicense.email'),
            disabled=True,
            width="medium"
        ),
        get_text('userLicense.userId'): st.column_config.TextColumn(
            get_text('userLicense.userId'),
            disabled=True,
            width="medium"
        ),
        get_text('userLicense.status'): st.column_config.SelectboxColumn(
            get_text('userLicense.status'),
            options=["active", "inactive"],
            width="small"
        ),
        get_text('userLicense.expirationDate'): st.column_config.TextColumn(
            get_text('userLicense.expirationDate'),
            disabled=True,
            width="medium"
        ),
        get_text('userLicense.lastLogin'): st.column_config.TextColumn(
            get_text('userLicense.lastLogin'),
            disabled=True,
            width="medium"
        ),
        get_text('userLicense.createdAt'): st.column_config.TextColumn(
            get_text('userLicense.createdAt'),
            disabled=True,
            width="medium"
        ),
        get_text('userLicense.updatedAt'): st.column_config.TextColumn(
            get_text('userLicense.updatedAt'),
            disabled=True,
            width="medium"
        )
    }

    # Display editable table
    edited_df = st.data_editor(
        df,
        column_config=column_config,
        hide_index=True,
        use_container_width=True,
        key="license_editor"
    )

    # Check for status changes
    if not df.equals(edited_df):
        for index, row in edited_df.iterrows():
            original_row = df.iloc[index]
            if row[get_text('userLicense.status')] != original_row[get_text('userLicense.status')]:
                email = row[get_text('userLicense.email')]
                new_status = row[get_text('userLicense.status')]
                if update_license_status(email, new_status):
                    st.rerun()

else:
    st.info(get_text('userLicense.noLicenses'))
