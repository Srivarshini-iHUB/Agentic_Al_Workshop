import streamlit as st
from crewai import Task, Crew, Process
import os
from agents import code_analyzer, code_corrector, manager
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="🐍 Python Code Reviewer", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        color: #4f46e5;
        margin-bottom: 0.2em;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        border-radius: 0.5rem;
        font-weight: 600;
        padding: 0.5em 1em;
    }
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🐍 AI-Powered Python Code Reviewer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Gemini + CrewAI to analyze and fix code without running it</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
### 📘 How It Works:
1. Paste your Python code in the box.
2. Click **Analyze & Fix Code**.
3. View the **issues**, **fixes**, and **final result** below.
""")

with st.expander("✍️ Paste Your Python Code", expanded=True):
    code_input = st.text_area("Write or paste Python code here:", height=300, placeholder="# Paste your code...")

if st.button("🚀 Analyze & Fix Code"):
    if not code_input.strip():
        st.warning("⚠️ Please enter Python code to proceed.")
    else:
        with st.spinner("🧠 Running multi-agent code review..."):

            analysis_task = Task(
                description=f"Analyze this code:\n```python\n{code_input}\n```",
                agent=code_analyzer,
                expected_output="List of static analysis issues and line-specific feedback."
            )

            correction_task = Task(
                description="Fix all the issues found in the code above. Preserve logic. Make the code PEP8 compliant.",
                agent=code_corrector,
                expected_output="Rewritten code with fixes and inline comments (if necessary).",
                context=[analysis_task]
            )
            crew = Crew(
                agents=[code_analyzer, code_corrector, manager],
                tasks=[analysis_task, correction_task],
                verbose=True,
                process=Process.sequential
            )
            result = crew.kickoff()

        st.success("✅ Analysis and Fix Completed!")

        st.subheader("📄 Code Review Output")
        with st.expander("🔍 View the full corrected code", expanded=True):
            st.code(result, language="python")

        st.markdown("---")
        st.markdown("💡 _This system performs static analysis only and doesn’t execute your code._")

else:
    st.info("👆 Paste your code above and hit 'Analyze & Fix Code'.")
