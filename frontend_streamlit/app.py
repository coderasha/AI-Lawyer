import streamlit as st
import requests

API_CHAT = "http://127.0.0.1:8000/chat"
API_UPLOAD = "http://127.0.0.1:8000/upload"

st.set_page_config(page_title="Legal AI Platform", page_icon="⚖️")

st.title("⚖️ Legal AI Platform")

# ---------------- SIDEBAR ---------------- #

st.sidebar.header("Settings")
mode = st.sidebar.selectbox("Mode", ["AUTO", "MANUAL"])

st.sidebar.divider()
st.sidebar.header("Upload Knowledge")

uploaded_file = st.sidebar.file_uploader(
    "Upload document",
    type=["pdf", "docx", "csv", "png", "jpg", "jpeg"]
)

if uploaded_file:
    with st.spinner("Learning document..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        res = requests.post(API_UPLOAD, files=files)

        if res.status_code == 200:
            st.sidebar.success("Document learned successfully!")
        else:
            st.sidebar.error("Upload failed")

# ---------------- CHAT MEMORY ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("meta"):
            st.caption(msg["meta"])

# ---------------- CHAT INPUT ---------------- #

if prompt := st.chat_input("Ask a legal question or type /learn ..."):

    # show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # learning command
    if prompt.startswith("/learn"):
        res = requests.post(API_CHAT, json={
            "message": prompt,
            "mode": mode,
            "model_name": "llama3"
        })
        st.success("Learned successfully")
        st.stop()

    # assistant response streaming
    with st.chat_message("assistant"):
        response_box = st.empty()
        full_text = ""

        try:
            with requests.post(
                API_CHAT,
                json={
                    "message": prompt,
                    "mode": mode,
                    "model_name": "llama3"
                },
                stream=True,
            ) as r:

                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        text = chunk.decode("utf-8")
                        full_text += text
                        response_box.markdown(full_text)

        except Exception as e:
            st.error(f"Backend not reachable: {e}")
            st.stop()

    # save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_text,
        "meta": f"Mode: {mode}"
    })
