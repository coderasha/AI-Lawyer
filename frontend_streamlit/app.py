import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="Legal AI", layout="wide")

# ---------------- STYLE ----------------

st.markdown("""
<style>
.chat-container {max-width: 900px; margin: auto;}
.user-msg {
    background: #DCF8C6;
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: right;
}
.ai-msg {
    background: #F1F0F0;
    padding: 12px;
    border-radius: 12px;
    margin: 8px 0;
    text-align: left;
}
.upload-box {
    border: 1px dashed #aaa;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("⚖️ Legal AI Assistant")

# ---------------- SESSION MEMORY ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- DISPLAY CHAT ----------------

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for role, msg in st.session_state.messages:
    if role == "user":
        st.markdown(f'<div class="user-msg">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-msg">{msg}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- INPUT AREA ----------------

col1, col2 = st.columns([8,1])

with col1:
    user_input = st.text_input("Message", label_visibility="collapsed", placeholder="Ask your legal question...")

with col2:
    uploaded_file = st.file_uploader("Attach", label_visibility="collapsed")

send = st.button("Send")

# ---------------- SEND MESSAGE ----------------

if send and user_input:

    # show user message
    st.session_state.messages.append(("user", user_input))
    st.rerun()

if len(st.session_state.messages) > 0 and st.session_state.messages[-1][0] == "user":

    prompt = st.session_state.messages[-1][1]

    files = {}
    data = {"message": prompt}

    if uploaded_file:
        files["file"] = (uploaded_file.name, uploaded_file.getvalue())

    # streaming request
    response = requests.post(API_URL, data=data, files=files, stream=True)

    ai_response = ""
    placeholder = st.empty()

    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            text = chunk.decode()
            ai_response += text
            placeholder.markdown(f'<div class="ai-msg">{ai_response}</div>', unsafe_allow_html=True)

    st.session_state.messages.append(("ai", ai_response))
    st.rerun()
