import streamlit as st
import requests
import base64

API_CHAT = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="Legal AI Platform", page_icon="⚖️")

st.title("⚖️ Legal AI Platform")

# ---------------- Session ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- Chat history ---------------- #

chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ---------------- Custom ChatGPT Input Bar ---------------- #

st.markdown("""
<style>
.chatbar {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    background: white;
    border-radius: 25px;
    border: 1px solid #ddd;
    padding: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.plus-btn {
    font-size: 22px;
    cursor: pointer;
    padding: 6px 12px;
    border-radius: 10px;
}

.input-box {
    flex-grow: 1;
    border: none;
    outline: none;
    font-size: 16px;
}

.send-btn {
    cursor: pointer;
    font-weight: bold;
}
</style>

<div class="chatbar">
    <span class="plus-btn">➕</span>
    <input id="msg" class="input-box" placeholder="Ask legal question..."/>
    <span class="send-btn">➤</span>
</div>
""", unsafe_allow_html=True)

# ---------------- Hidden uploader ---------------- #

uploaded_file = st.file_uploader(
    "Upload file",
    type=["png","jpg","jpeg","pdf","docx"],
    label_visibility="collapsed"
)

# ---------------- Message Input ---------------- #

prompt = st.text_input("hidden", label_visibility="collapsed")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)

    files = None
    if uploaded_file:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}

    with chat_container:
        with st.chat_message("assistant"):
            response_box = st.empty()
            full_text = ""

            with requests.post(
                API_CHAT,
                data={"message": prompt, "mode": "AUTO", "model_name": "llama3"},
                files=files,
                stream=True,
            ) as r:

                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        text = chunk.decode("utf-8")
                        full_text += text
                        response_box.markdown(full_text)

    st.session_state.messages.append({"role": "assistant", "content": full_text})
