import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from rag import create_vector_store, create_qa_chain

# ─────────────────────────────
# Load env
# ─────────────────────────────
load_dotenv()
api_key = os.getenv("GROQ_API_KEY", "")
os.environ["GROQ_API_KEY"] = api_key

# ─────────────────────────────
# Page config
# ─────────────────────────────
st.set_page_config(
    page_title="DocuMind AI 🌿",
    page_icon="🌿",
    layout="wide"
)

# ─────────────────────────────
# Soft pastel UI theme
# ─────────────────────────────
st.markdown("""
<style>

html, body {
    background-color: #f7f8fc;
}

/* Hide streamlit style noise */
#MainMenu, footer, header {visibility: hidden;}

/* Title */
.title {
    text-align: center;
    font-size: 40px;
    font-weight: 700;
    background: linear-gradient(90deg, #7c9cff, #a78bfa, #6ee7b7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
}

.subtitle {
    text-align: center;
    color: #6b7280;
    font-size: 16px;
    margin-bottom: 25px;
}

/* Chat bubbles */
.user-bubble {
    background: #dbeafe;
    padding: 12px 16px;
    border-radius: 18px;
    margin: 8px 0;
    max-width: 75%;
    margin-left: auto;
    color: #111827;
}

.bot-bubble {
    background: #ffffff;
    padding: 12px 16px;
    border-radius: 18px;
    margin: 8px 0;
    max-width: 75%;
    border: 1px solid #e5e7eb;
    color: #111827;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #eee;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #7c9cff, #a78bfa);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.5rem 1rem;
    font-weight: 500;
}

.stButton>button:hover {
    transform: scale(1.02);
}

/* Chat input */
.stChatInput textarea {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────
# Header
# ─────────────────────────────
st.markdown("<div class='title'>DocuMind AI 🌿</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your calm, friendly AI study companion for any PDF ✨</div>", unsafe_allow_html=True)

# ─────────────────────────────
# Session state
# ─────────────────────────────
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

if "chat" not in st.session_state:
    st.session_state.chat = []

# ─────────────────────────────
# Sidebar
# ─────────────────────────────
with st.sidebar:
    st.title("🌿 Setup")

    if api_key:
        st.success("API key loaded 🌟")
    else:
        st.warning("Add GROQ_API_KEY in .env")

    st.markdown("---")

    uploaded_file = st.file_uploader("Upload your PDF 📄", type=["pdf"])

    if uploaded_file and not st.session_state.qa_chain:
        with st.spinner("Reading your document... 📖"):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    path = tmp.name

                vectorstore = create_vector_store(path)
                st.session_state.qa_chain = create_qa_chain(vectorstore)

                st.success("Ready to chat 💬")
            except Exception as e:
                st.error(f"Oops: {e}")

    st.markdown("---")
    st.caption("Tip: Ask simple questions first for better answers ✨")

# ─────────────────────────────
# Chat UI
# ─────────────────────────────
if st.session_state.qa_chain:

    for msg in st.session_state.chat:

        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'>🧑‍🎓 {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-bubble'>🌿 {msg['content']}</div>", unsafe_allow_html=True)

    query = st.chat_input("Ask something from your PDF...")

    if query:

        # user message
        st.session_state.chat.append({"role": "user", "content": query})
        st.markdown(f"<div class='user-bubble'>🧑‍🎓 {query}</div>", unsafe_allow_html=True)

        with st.spinner("Thinking... 🤔"):

            try:
                answer = st.session_state.qa_chain.invoke({
                    "question": query
                })

            except Exception as e:
                answer = f"Something went wrong: {e}"

        # bot message
        st.session_state.chat.append({"role": "assistant", "content": answer})
        st.markdown(f"<div class='bot-bubble'>🌿 {answer}</div>", unsafe_allow_html=True)

else:
    st.info("👈 Upload a PDF to start your study session")