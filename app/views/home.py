import streamlit as st
from forms.login import login_form, signup_form

@st.dialog("Đăng nhập")
def show_login_form():
    login_form()

@st.dialog("Đăng kí")
def show_signup_form():
    signup_form()
    
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("app/access/logo.jpeg", width=230)
    if st.button("Đăng kí"):
        show_signup_form()
    if st.button("Đăng nhập"):
        show_login_form()
with col2:
    st.title("Hoàng Hà Mobile", anchor=False)