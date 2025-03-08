import json
from typing import Any
import uuid
import streamlit as st
import time
from streamlit_js import st_js

KEY_PREFIX = "st_localstorage_"

class StLocalStorage:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        # Keep track of a UUID for each key to enable reruns
        if "_ls_unique_keys" not in st.session_state:
            st.session_state["_ls_unique_keys"] = {}
        # Hide the JS iframes
        self._container = st.container()
        with self._container:
            st.html(""" 
                <style>
                    .element-container:has(iframe[height="0"]) {
                        display: none;
                    }
                </style>
            """)

    def __getitem__(self, key: str) -> Any:
        if key not in st.session_state["_ls_unique_keys"]:
            st.session_state["_ls_unique_keys"][key] = str(uuid.uuid4())
        code = f"""
        console.log('{st.session_state["_ls_unique_keys"][key]}');
        return JSON.parse(localStorage.getItem('{KEY_PREFIX + key}'));
        """
        with self._container:
            result = st_js(code, key=st.session_state["_ls_unique_keys"][key])
            time.sleep(0.3)
        if result and result[0]:
            result_val = result[0]
            st.session_state[key] = result_val
            return result_val
        return None

    def __setitem__(self, key: str, value: Any) -> None:
        if "_ls_unique_keys" not in st.session_state:
            st.session_state["_ls_unique_keys"] = {}
        value_json = json.dumps(value, ensure_ascii=False)
        st.session_state["_ls_unique_keys"][key] = str(uuid.uuid4())
        code = f"""
        console.log('setting {key} to local storage');
        localStorage.setItem('{KEY_PREFIX + key}', JSON.stringify({value_json}));
        """
        try:
            with self._container:
                st.session_state[key] = value
                return st_js(code, key=st.session_state["_ls_unique_keys"][key] + "_set")
        except Exception as e:
            print('Err: ', e)

    def __delitem__(self, key: str) -> None:
        st.session_state["_ls_unique_keys"][key] = str(uuid.uuid4())
        code = f"localStorage.removeItem('{KEY_PREFIX + key}');"
        with self._container:
            st.session_state.pop(key, None)
            return st_js(code, key=st.session_state["_ls_unique_keys"][key] + "_del")

    def __contains__(self, key: str) -> bool:
        return self.__getitem__(key) is not None

    def get(self, key: str, cached = True) -> Any:
        if cached:
            if key in st.session_state:
                return st.session_state[key]
        try:
            return self.__getitem__(key)
        except:
            return None

    def set(self, key: str, value: Any) -> None:
        try:
            self.__setitem__(key, value)
        except Exception as e:
            print(e)
            return None
    
    def delete(self, key: str) -> None:
        try:
            self.__delitem__(key)
        except Exception as e:
            print(e)
            return None

