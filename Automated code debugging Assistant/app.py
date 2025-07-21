import streamlit as st
from crewai import Task, Crew, Process
import os

from utils import analyze_python_code
from agents import code_analyzer, code_corrector, manager

# Set Google API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyAC1wHxDXyDGPdBfMvD6H76iA0L7cS7iU8"

# ----- Streamlit UI -----
st.set_page_config(page_title="Python Code Reviewer", page_icon="🐍", layout="centered")
st.title("🐍 AI-Powered Python Code Reviewer")

st.markdown(
    """
    Welcome to the AI-Powered Python Code Reviewer! This tool helps you analyze and fix your Python code using AI-powered agents without executing the code.
    
    **How to use:**
    1. Paste your Python code in the input box below.
    2. Click the 'Analyze & Fix Code' button.
    3. View the analysis results and suggested fixes.
    """
)

# Input Section
with st.expander("📥 Paste Your Python Code", expanded=True):
    code_input = st.text_area("Write or paste your Python code below:", height=300, placeholder="# Your Python code here...")

# Action
if st.button("🚀 Analyze & Fix Code"):
    if not code_input.strip():
        st.warning("Please enter Python code to proceed.")
    else:
        with st.spinner("🤖 Running static analysis and corrections..."):

            # Tasks
            analysis_task = Task(
                description=f"Analyze this code:\n```python\n{code_input}\n```",
                agent=code_analyzer,
                expected_output="List of static analysis issues."
            )

            correction_task = Task(
                description="Fix all issues found.",
                agent=code_corrector,
                expected_output="Corrected Python code with explanations.",
                context=[analysis_task]
            )

            # CrewAI Execution
            crew = Crew(
                agents=[code_analyzer, code_corrector, manager],
                tasks=[analysis_task, correction_task],
                verbose=True,
                process=Process.sequential
            )

            result = crew.kickoff()

        # Output Section
        st.success("✅ Analysis and Fix Completed!")
        st.subheader("🔍 Code Review Result")
        st.code(result, language="python")

# Footer
st.markdown("---")
st.markdown("💡 _Built using [CrewAI](https://docs.crewai.com) and Gemini for static analysis and code correction._")
