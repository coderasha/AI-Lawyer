import streamlit as st
import requests

API_CHAT = "http://127.0.0.1:8000/chat"
API_UPLOAD = "http://127.0.0.1:8000/upload"

st.set_page_config(page_title="Legal AI Platform", page_icon="⚖️")

st.title("⚖️ Legal AI Platform")

# ---------------- Session State ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "show_uploader" not in st.session_state:
    st.session_state.show_uploader = False

if "chat_file" not in st.session_state:
    st.session_state.chat_file = None

# ---------------- Sidebar permanent learning ---------------- #

st.sidebar.header("Teach AI (Permanent Knowledge)")

knowledge_file = st.sidebar.file_uploader(
    "Upload lawbook / contract permanently",
    type=["pdf", "docx", "csv", "png", "jpg", "jpeg"]
)

if knowledge_file:
    with st.spinner("Learning document permanently..."):
        files = {"file": (knowledge_file.name, knowledge_file.getvalue())}
        res = requests.post(API_UPLOAD, files=files)

        if res.status_code == 200:
            st.sidebar.success("Document learned!")
        else:
            st.sidebar.error("Upload failed")

# ---------------- Chat history ---------------- #

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- Attachment Button ---------------- #

col1, col2 = st.columns([1, 12])

with col1:
    if st.button("➕"):
        st.session_state.show_uploader = not st.session_state.show_uploader

# popup uploader
if st.session_state.show_uploader:
    st.session_state.chat_file = st.file_uploader(
        "Add photos & files",
        type=["png", "jpg", "jpeg", "pdf", "docx"],
        key="chat_attach"
    )

# ---------------- Chat Input ---------------- #

prompt = st.chat_input("Ask legal question...")

if prompt:

    # show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # prepare file
    files = None
    if st.session_state.chat_file:
        files = {
            "file": (
                st.session_state.chat_file.name,
                st.session_state.chat_file.getvalue()
            )
        }

    # streaming response
    with st.chat_message("assistant"):
        response_box = st.empty()
        full_text = ""

        with requests.post(
            API_CHAT,
            data={
                "message": prompt,
                "mode": "AUTO",
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

    # save message
    st.session_state.messages.append({"role": "assistant", "content": full_text})

    # reset attachment
    st.session_state.chat_file = None
    st.session_state.show_uploader = False
