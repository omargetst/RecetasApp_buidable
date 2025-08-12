import streamlit as st

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "history" not in st.session_state:
        st.session_state.history = []
    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "centered"
    if "input_buffer" not in st.session_state:
        st.session_state.input_buffer = ""
