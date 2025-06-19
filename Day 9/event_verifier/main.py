import streamlit as st
import os
from tools.file_tools import load_student_inputs
from agents.evidence_extractor import evidence_chain
from agents.participation_verifier import verifier_chain
from agents.learning_outcome_extractor import learning_outcome_chain
from agents.session_alignment_agent import get_session_alignment_chain

st.set_page_config(page_title="🎓 Industry Event Participation Verifier", layout="wide")
st.title("🎓 Industry Event Participation Verifier (LangChain + Gemini)")

# Create folders
os.makedirs("uploads/inputs", exist_ok=True)
os.makedirs("data", exist_ok=True)

# -------------------- Admin: Upload Official Session Document --------------------
with st.expander("🛠️ Admin Only: Upload Official Session Document"):
    uploaded_session_doc = st.file_uploader("📘 Upload Official Event Session Document (TXT)", type=["txt"], key="session_doc")
    if uploaded_session_doc:
        session_path = os.path.join("data", "session.txt")
        with open(session_path, "wb") as f:
            f.write(uploaded_session_doc.read())
        st.success("✅ Official session document saved to `data/session.txt`.")

# -------------------- Student Evidence Upload --------------------
with st.sidebar:
    st.header("📤 Upload Files")
    input_files = st.file_uploader("📝 Upload Student Evidence (ticket, LinkedIn post, notes)", accept_multiple_files=True)

# -------------------- Verify Button --------------------
if st.button("🧠 Run Verification"):

    if not input_files:
        st.error("Please upload student evidence files.")
        st.stop()

    session_path = os.path.join("data", "session.txt")
    if not os.path.exists(session_path):
        st.error("❌ Session document not found in `data/session.txt`. Please upload it using the Admin section.")
        st.stop()

    # Save student evidence
    for f in input_files:
        input_path = os.path.join("uploads/inputs", f.name)
        with open(input_path, "wb") as out_file:
            out_file.write(f.read())

    st.info("⏳ Processing student evidence...")

    # Load and preview student notes
    input_text = load_student_inputs("uploads/inputs")
    with st.expander("📎 Preview: Combined Student Inputs"):
        st.text(input_text[:2000])

    # -------------------- Step 1: Evidence Extraction --------------------
    st.subheader("🔍 Step 1: Evidence Extraction")
    evidence = evidence_chain().run(input_text)
    st.success(evidence)

    # -------------------- Step 2: Participation Verification --------------------
    st.subheader("✅ Step 2: Participation Verification")
    verified = verifier_chain().run(evidence)
    st.success(verified)

    # -------------------- Step 3: Learning Outcome Extraction --------------------
    st.subheader("🧠 Step 3: Learning Outcome Extraction")
    learnings = learning_outcome_chain().run(input_text)
    st.success(learnings)

    # -------------------- Step 4: Session Alignment (RAG) --------------------
    st.subheader("📚 Step 4: Session Alignment (RAG)")
    rag_chain = get_session_alignment_chain(session_path)
    alignment = rag_chain.run(learnings)
    st.success(alignment)
