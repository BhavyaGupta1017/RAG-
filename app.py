import streamlit as st
from main import build_vector_store, answer_question

st.set_page_config(page_title="Chat with your PDF | RAG", page_icon="📚", layout="wide")

st.title("📚 Chat with your PDF")
st.caption("Upload a PDF, ask questions, and get answers grounded in your document.")

with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Gemini API key", type="password",
                            help="Your key is used only for this session. For deployment, use Streamlit Secrets.")
    st.markdown("---")
    st.markdown("**How it works**")
    st.write("PDF → text extraction → chunks → embeddings → FAISS retrieval → Gemini answer")
    st.caption("Tip: scanned/image-only PDFs may need OCR before their text can be searched.")

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "document_name" not in st.session_state:
    st.session_state.document_name = None
if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

col1, col2 = st.columns([1, 3])
with col1:
    process = st.button("Process PDF", type="primary", disabled=uploaded_file is None)
with col2:
    if st.session_state.document_name:
        st.success(f"Loaded: {st.session_state.document_name}")

if process and uploaded_file:
    with st.spinner("Reading PDF and creating the searchable index..."):
        try:
            st.session_state.vector_store = build_vector_store(uploaded_file.getvalue())
            st.session_state.document_name = uploaded_file.name
            st.session_state.messages = []
            st.success("PDF processed! You can ask questions below.")
        except Exception as exc:
            st.error(f"Could not process this PDF: {exc}")

st.divider()
st.subheader("💬 Ask questions")

if st.session_state.vector_store is None:
    st.info("Upload a PDF and click **Process PDF** to begin.")
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("sources"):
                with st.expander("Sources used"):
                    for source in message["sources"]:
                        st.write(f"Page {source['page']}: {source['text']}")

    question = st.chat_input("Ask something about your PDF...")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        key = api_key.strip()
        if not key:
            try:
                key = st.secrets["GEMINI_API_KEY"]
            except Exception:
                key = ""

        if not key:
            st.warning("Enter your Gemini API key in the sidebar, or add GEMINI_API_KEY to Streamlit Secrets.")
        else:
            with st.chat_message("assistant"):
                with st.spinner("Searching your PDF and generating an answer..."):
                    try:
                        answer, sources = answer_question(
                            question, st.session_state.vector_store, key
                        )
                        st.markdown(answer)
                        if sources:
                            with st.expander("Sources used"):
                                for source in sources:
                                    st.markdown(f"**Page {source['page']}**")
                                    st.write(source["text"])
                        st.session_state.messages.append({
                            "role": "assistant", "content": answer, "sources": sources
                        })
                    except Exception as exc:
                        st.error(f"Something went wrong: {exc}")

st.caption("Answers are generated from retrieved PDF passages. Always verify important information against the original document.")
