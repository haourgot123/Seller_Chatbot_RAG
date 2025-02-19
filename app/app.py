import streamlit as st



home = st.Page(
    "views/home.py",
    title = "Trang chủ",
    icon = ":material/account_circle:",
    default = True
)
chatbot = st.Page(
    "views/chatbot.py",
    title = "Chat với Nhân Viên Tư Vấn",
    icon = ":material/smart_toy:"
)
pg = st.navigation(
    {
        "Hoàng Hà Mobile": [home],
        "Chatbot": [chatbot]
    }
)

pg.run()
