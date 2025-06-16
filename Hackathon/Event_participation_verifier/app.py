import streamlit as st
from dotenv import load_dotenv
import os

from verifier.linkedin_parser import extract_linkedin_info
from verifier.notes_rag import setup_rag, evaluate_alignment
from verifier.pdf_verifier import verify_event_ticket
from verifier.ocr_screenshot import extract_text_from_image

# Load .env for Gemini API key
load_dotenv()

st.set_page_config(page_title="Industry Event Participation Verifier", layout="centered")
st.title("Industry Event Participation Verifier")

st.markdown("Upload evidence to verify your participation in a tech event like NASSCOM, Google DevFest, etc.")

# --- Upload Ticket PDF ---
ticket = st.file_uploader("Upload DevFest Ticket PDF", type=["pdf"])
if ticket:
    ticket_valid, ticket_keywords = verify_event_ticket(ticket)
    if ticket_valid:
        st.success("✅ Ticket Verified with keywords: " + ", ".join(ticket_keywords))
    else:
        st.warning("⚠️ Could not verify ticket content. Please ensure it includes event keywords.")

# --- Upload LinkedIn Screenshot ---
screenshot = st.file_uploader("Upload LinkedIn Screenshot (optional)", type=["png", "jpg", "jpeg"])
if screenshot:
    ocr_text = extract_text_from_image(screenshot)
    st.text_area("📝 OCR Extracted Text", ocr_text, height=200)
    li_summary = extract_linkedin_info(ocr_text)
    st.info(f"🔍 Extracted Summary from LinkedIn: {li_summary}")

# --- Upload Student Notes ---
student_notes = st.text_area("✍️ Paste Your Notes / Learnings from the Event")

# --- RAG Verification ---
if screenshot and student_notes:
    st.markdown("---")
    if st.button("✅ Verify Learning with AI"):
        try:
            with open("data/reference_docs.txt", "r", encoding="utf-8") as f:
                reference_text = f.read()
        except FileNotFoundError:
            st.error("❌ Reference file not found. Please ensure `data/reference_docs.txt` exists.")
        else:
            qa_context = setup_rag(reference_text)
            rag_result = evaluate_alignment(qa_context, student_notes)
            st.subheader("🤖 AI Evaluation Result")
            st.success(rag_result)
