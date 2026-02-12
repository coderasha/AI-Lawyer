import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="Legal AI Platform", page_icon="⚖️")

st.title("⚖️ Legal AI Platform")

# session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# mode selection
mode = st.sidebar.selectbox("Mode", ["AUTO", "MANUAL"])

# display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            st.caption(f"Model: {msg.get('model')} | Confidence: {msg.get('confidence')}")

# user input
if prompt := st.chat_input("Ask legal question or type /learn ..."):

    # show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # call backend
    try:
        res = requests.post(API_URL, json={
            "message": prompt,
            "mode": mode,
            "model_name": "llama3"
        })

        data = res.json()

        response_text = data.get("response", data.get("status"))

        # show AI response
        with st.chat_message("assistant"):
            st.write(response_text)

            if "model_used" in data:
                st.caption(f"Model: {data['model_used']} | Confidence: {data['confidence']}")

        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text,
            "model": data.get("model_used"),
            "confidence": data.get("confidence")
        })

    except Exception as e:
        st.error(f"Backend not reachable: {e}")
