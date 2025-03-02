import json
import os
from typing import Dict, Any
import streamlit as st
from st_local_storage import StLocalStorage

class I18n:
    def __init__(self):
        self.translations: Dict[str, Dict[str, Any]] = {}
        self.load_translations()
        self.local_storage = StLocalStorage()
        
    def load_translations(self):
        locales_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locales')
        for file in os.listdir(locales_dir):
            if file.endswith('.json'):
                language = file.split('.')[0]
                with open(os.path.join(locales_dir, file), 'r', encoding='utf-8') as f:
                    self.translations[language] = json.load(f)
    
    def get_text(self, key: str, language: str = None) -> str:
        """
        Get translated text for a given key and language.
        Key format: 'section.subsection.key' (e.g., 'common.welcome')
        """
        if language is None:
            # Try to get language from local storage first
            stored_lang = self.local_storage.get('language')
            if stored_lang:
                language = stored_lang
            else:
                language = st.session_state.get('language', 'en')
            
        if language not in self.translations:
            language = 'en'
            
        keys = key.split('.')
        value = self.translations[language]
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return key
                
        return value

# Create a singleton instance
i18n = I18n()

def get_text(key: str, language: str = None) -> str:
    """Helper function to get translated text"""
    return i18n.get_text(key, language)

def set_language(language: str):
    """Set the current language in session state and local storage"""
    st.session_state['language'] = language
    i18n.local_storage.set('language', language)

def get_available_languages() -> list:
    """Get list of available languages"""
    return list(i18n.translations.keys())
