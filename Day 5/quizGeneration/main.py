import os
import streamlit as st
from dotenv import load_dotenv
from utils import extract_text_from_pdf
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0.7)

# Streamlit UI
st.set_page_config(page_title="Study Assistant", layout="centered")
st.title("📘 Study Assistant: Summarizer + Quiz Generator")
st.markdown("Upload a study material PDF to summarize and generate a full set of quiz questions.")

# Upload PDF
pdf_file = st.file_uploader("Upload your course material (PDF)", type="pdf")

if pdf_file:
    with open("temp.pdf", "wb") as f:
        f.write(pdf_file.read())

    # Extract text from PDF
    study_text = extract_text_from_pdf("temp.pdf")

    st.subheader("📄 Extracted Study Material")
    st.text_area("Raw Text:", study_text, height=200)

    # Prompt templates
    summary_prompt = PromptTemplate(
        input_variables=["content"],
        template="""
Summarize the following study material into concise bullet points.

Content:
{content}

Summary:
"""
    )

    quiz_prompt = PromptTemplate(
        input_variables=["summary"],
        template="""
Based on the summarized content below, generate at least 10 multiple-choice quiz questions. 
Each question should have:
- A clear question statement
- Four answer options (a, b, c, d)
- The correct answer clearly indicated below each question

Summary:
{summary}

Format:
Q1. ...
a)
b)
c)
d)
Answer: ...

Q2. ...
a)
b)
c)
d)
Answer: ...
"""
    )

    # Button to trigger processing
    if st.button("🧠 Generate Summary & Quiz"):
        with st.spinner("Processing..."):
            # Run summarization chain
            summary_chain = LLMChain(llm=llm, prompt=summary_prompt)
            summary = summary_chain.run(content=study_text)

            # Run quiz generation chain
            quiz_chain = LLMChain(llm=llm, prompt=quiz_prompt)
            quiz = quiz_chain.run(summary=summary)

        st.subheader("📝 Summary")
        st.markdown(summary)

        st.subheader("🧪 Quiz Questions")
        st.markdown(quiz)
