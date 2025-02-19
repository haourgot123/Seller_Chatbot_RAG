import streamlit as st


def login_form():
    with st.form("Đăng nhập"):
        email = st.text_input("Email Address")
        password = st.text_input("Password")
        summit_button = st.form_submit_button("Đăng nhập")
    if summit_button:
        if not email:
            st.error("Please provide your email address.", icon="📨")
            st.stop()
        if not password:
            st.error("Please provide your password.", icon="📨")
            st.stop()

def signup_form():
    with st.form("Đăng kí"):
        email = st.text_input("Email Adrress")
        phone_number = st.text_input("Phone Number")
        password = st.text_input("Password")
        retype_password = st.text_input("Retype Password")
        summit_button = st.form_submit_button("Đăng kí")
    if summit_button:
        if not email:
            st.error("Please provide your email address.", icon="📨")
            st.stop()
        if not phone_number:
            st.error("Please provide your phone number.", icon="📨")
            st.stop()
        if not password:
            st.error("Please provide your password", icon="📨")
            st.stop()
        if not retype_password:
            st.error("Please provide your password", icon="📨")
            st.stop()
        if password != retype_password:
            st.error("Passwords do not match", icon="📨")
            st.stop()
        if password == retype_password:
            st.success("Password matches")
    