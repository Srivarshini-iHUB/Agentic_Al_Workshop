import streamlit as st
from agents.evidence_extractor import extract_evidence
from agents.participation_verifier import verify_participation
from agents.learning_outcome_extractor import extract_learning
from agents.session_alignment_agent import align_sessions

st.set_page_config(page_title="Industry Event OKR Verifier", layout="centered")
st.title("📊 Industry Event Participation Verifier")
st.markdown("Upload proof of event attendance and learning notes to verify OKRs.")

uploaded_files = st.file_uploader("📁 Upload Evidence (Ticket PDFs, LinkedIn screenshots, etc.)", accept_multiple_files=True)
user_notes = st.text_area("📝 Paste Your Learning Notes or Reflections")
event_name = st.text_input("📌 Event Name (e.g., NASSCOM DevFest)")
submit = st.button("🔍 Run Verification")

if submit:
    if not uploaded_files or not event_name:
        st.error("🚫 Please upload at least one file and enter the event name.")
    else:
        with st.spinner("🔍 Extracting evidence..."):
            evidence_json = extract_evidence(uploaded_files)
        st.success("✅ Evidence extracted.")
        st.json(evidence_json)

        with st.spinner("🔍 Verifying participation..."):
            verified = verify_participation(evidence_json)
        st.success(f"✅ Participation status: {'Verified' if verified else 'Not Verified'}")

        with st.spinner("📖 Extracting learning outcomes..."):
            learnings = extract_learning(user_notes)
        st.success("✅ Learning outcomes extracted.")
        st.markdown(f"**🧠 Key Learnings:**\n\n{learnings}")

        with st.spinner("📚 Aligning with official sessions..."):
            alignment = align_sessions(event_name, learnings)
        st.success("✅ Session alignment complete.")
        st.markdown(f"**🎯 Session Alignment Result:**\n\n{alignment}")

        st.markdown("---")
        st.markdown("### 📋 Final Summary")
        st.json({
            "Participation Verified": verified,
            "Extracted Learnings": learnings,
            "Session Alignment": alignment,
            "Extracted Evidence": evidence_json
        })
