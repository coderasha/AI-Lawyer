import streamlit as st
import requests

API_CHAT = "http://127.0.0.1:8000/chat"
API_UPLOAD = "http://127.0.0.1:8000/upload"

st.set_page_config(page_title="Legal AI Platform", page_icon="⚖️")

st.title("⚖️ Legal AI Platform")

# ---------------- SIDEBAR SETTINGS ---------------- #

st.sidebar.header("Settings")
mode = st.sidebar.selectbox("Mode", ["AUTO", "MANUAL"])

# -------- Permanent Knowledge Upload -------- #

st.sidebar.divider()
st.sidebar.header("Teach AI (Permanent Memory)")

knowledge_file = st.sidebar.file_uploader(
    "Upload lawbook / contract / evidence",
    type=["pdf", "docx", "csv", "png", "jpg", "jpeg"],
    key="knowledge_upload"
)

if knowledge_file:
    with st.spinner("Learning document permanently..."):
        files = {"file": (knowledge_file.name, knowledge_file.getvalue())}
        res = requests.post(API_UPLOAD, files=files)

        if res.status_code == 200:
            st.sidebar.success("Document permanently learned!")
        else:
            st.sidebar.error("Upload failed")

# ---------------- CHAT MEMORY ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

# display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------- Temporary Chat File Upload -------- #

st.divider()
st.caption("Attach file for this question (optional, not saved permanently)")

chat_file = st.file_uploader(
    "Attach image/pdf/docx",
    type=["png", "jpg", "jpeg", "pdf", "docx"],
    key="chat_file"
)

# ---------------- CHAT INPUT ---------------- #

if prompt := st.chat_input("Ask legal question or type /learn ..."):

    # show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # handle learning command
    if prompt.startswith("/learn"):
        res = requests.post(API_CHAT, data={
            "message": prompt,
            "mode": mode,
            "model_name": "llama3"
        })
        st.success("Learned successfully")
        st.stop()

    # -------- Assistant streaming response -------- #

    with st.chat_message("assistant"):
        response_box = st.empty()
        full_text = ""

        files = None
        if chat_file:
            files = {"file": (chat_file.name, chat_file.getvalue())}

        try:
            with requests.post(
                API_CHAT,
                data={
                    "message": prompt,
                    "mode": mode,
                    "model_name": "llama3"
                },
                files=files,
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
        "content": full_text
    })
