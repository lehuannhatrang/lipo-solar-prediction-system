import streamlit as st
from utils.i18n import set_language, get_available_languages
from st_local_storage import StLocalStorage

def language_selector():
    """Language selector component"""
    languages = {
        'en': 'English',
        'vi': 'Tiếng Việt',
        'ko': '한국어'
    }
    
    # Initialize local storage
    local_storage = StLocalStorage()
    
    # Try to get language from local storage first
    stored_lang = local_storage.get('language')
    if stored_lang and stored_lang not in st.session_state:
        st.session_state['language'] = stored_lang
    
    current_lang = st.session_state.get('language', 'en')
    
    # Create a select box for language selection
    selected_lang = st.selectbox(
        'Language',
        options=get_available_languages(),
        format_func=lambda x: languages.get(x, x),
        index=get_available_languages().index(current_lang)
    )
    
    # Update language if changed
    if selected_lang != current_lang:
        set_language(selected_lang)
