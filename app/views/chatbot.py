import os
import sys
from groq import Groq
import streamlit as st
from configs.config import LoadConfig
from rag.rag_based import RAG
CONFIG_APP = LoadConfig()

def parse_groq_stream(stream):
    for chunk in stream:
        if chunk.choices:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content


if "model" not in st.session_state:
    st.session_state["model"] =Groq(api_key = CONFIG_APP.GROQ_API)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Chào anh/chị ạ. Em có thể giúp gì cho anh/chị không ạ?"}]


for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Nhập câu hỏi của bạn"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message('assistant'):
        client = st.session_state["model"]
        stream = client.chat.completions.create(
            model = CONFIG_APP.GROQ_MODEL,
            messages = [
                {"role": message["role"], "content": message["content"]} for message in st.session_state["messages"]
            ],
            temperature = CONFIG_APP.GROQ_TEMPERATURE,
            max_tokens = CONFIG_APP.GROQ_MAX_TOKENS,
            stream = True
        )
        response = st.write_stream(parse_groq_stream(stream))
    st.session_state['messages'].append({"role": "assistant", "content": response})
