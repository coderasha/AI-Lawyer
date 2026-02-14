import streamlit as st
import requests

CHAT_API = "http://127.0.0.1:8000/chat"
UPLOAD_API = "http://127.0.0.1:8000/upload"

st.set_page_config(layout="wide", page_title="Legal AI")

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "processing" not in st.session_state:
    st.session_state.processing = False

if "send_trigger" not in st.session_state:
    st.session_state.send_trigger = False

if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""

# ---------------- SIDEBAR TRAINING ----------------
with st.sidebar:
    st.title("📚 Teach AI (Permanent Memory)")

    train_file = st.file_uploader(
        "Upload law books, notices, agreements",
        type=["pdf","docx","txt","csv","png","jpg","jpeg"],
        key="train_upload"
    )

    if st.button("Train AI") and train_file:
        with st.spinner("Teaching AI..."):
            files = {"file": (train_file.name, train_file.getvalue())}
            res = requests.post(UPLOAD_API, files=files)

            if res.status_code == 200:
                st.success(f"Learned: {train_file.name}")
            else:
                st.error("Training failed")

    st.markdown("---")
    st.info("Files uploaded here become permanent knowledge")

# ---------------- CHAT DISPLAY ----------------
st.title("⚖️ Legal AI Assistant")

for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(msg)

# ---------------- TEMP FILE ATTACH ----------------
uploaded = st.file_uploader(
    "Attach file for this question",
    type=["pdf","docx","txt","csv","png","jpg","jpeg"],
    key="chat_upload",
    label_visibility="collapsed"
)

# ---------------- INPUT HANDLING ----------------
prompt = st.chat_input("Ask legal question...", key="prompt_box")

if prompt:
    st.session_state.current_prompt = prompt
    st.session_state.send_trigger = True
    st.rerun()

# ---------------- PROCESS MESSAGE ----------------
if st.session_state.get("send_trigger", False):

    st.session_state.processing = True
    user_prompt = st.session_state.current_prompt

    # show user message
    st.session_state.messages.append(("user", user_prompt))
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # prepare request
    data = {"message": user_prompt}
    files = {}

    if uploaded:
        files["file"] = (uploaded.name, uploaded.getvalue())

    # assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            with st.spinner("Legal AI is thinking..."):
                response = requests.post(CHAT_API, data=data, files=files, stream=True)

                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        text = chunk.decode()
                        full_response += text
                        message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        except Exception:
            full_response = "⚠️ Backend not reachable. Start FastAPI server."
            message_placeholder.markdown(full_response)

    st.session_state.messages.append(("assistant", full_response))

    # reset
    st.session_state.processing = False
    st.session_state.send_trigger = False
    st.session_state.current_prompt = ""

    st.rerun()