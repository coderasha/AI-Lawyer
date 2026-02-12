import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.title("⚖️ Legal AI Platform")

if "messages" not in st.session_state:
    st.session_state.messages = []

mode = st.sidebar.selectbox("Mode", ["AUTO", "MANUAL"])

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask a legal question..."):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""

        with requests.post(API_URL, json={
            "message": prompt,
            "mode": mode,
            "model_name": "llama3"
        }, stream=True) as r:

            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    text = chunk.decode("utf-8")
                    full_response += text
                    response_container.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
