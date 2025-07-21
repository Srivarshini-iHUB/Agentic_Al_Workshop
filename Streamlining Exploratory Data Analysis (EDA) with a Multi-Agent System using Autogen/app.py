import os
import pandas as pd
import streamlit as st
import google.generativeai as genai
from autogen.agentchat import (
    AssistantAgent,
    UserProxyAgent,
    GroupChat,
    GroupChatManager,
)
from dotenv import load_dotenv
load_dotenv()

# ------------------------ API CONFIG ------------------------
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")
genai.configure(api_key=api_key)

# ------------------------ GEMINI CALL ------------------------
def gemini_call(prompt, model_name="models/gemini-1.5-flash"):
    return genai.GenerativeModel(model_name).generate_content(prompt).text

# ------------------------ AGENT DEFINITIONS ------------------------
class DataPrepAgent(AssistantAgent):
    def generate_reply(self, messages, sender, config=None):
        df = st.session_state["df"]
        prompt = f"""You are a Data Cleaning Agent.
- Handle missing values
- Fix data types
- Remove duplicates

Dataset head:
{df.head().to_string()}

Summary stats:
{df.describe(include='all').to_string()}

Return Python code for preprocessing and a short explanation."""
        return gemini_call(prompt)

class EDAAgent(AssistantAgent):
    def generate_reply(self, messages, sender, config=None):
        df = st.session_state["df"]
        prompt = f"""You are an EDA Agent.
- Provide summary statistics
- Extract at least 3 insights
- Suggest visualizations

Dataset head:
{df.head().to_string()}"""
        return gemini_call(prompt)

class ReportGeneratorAgent(AssistantAgent):
    def generate_reply(self, messages, sender, config=None):
        insights = st.session_state.get("eda_output", "")
        prompt = f"""You are a Report Generator.
Create a clean EDA report based on insights:

{insights}

Include:
- Overview
- Key Findings
- Visual Suggestions
- Summary conclusion."""
        return gemini_call(prompt)

class CriticAgent(AssistantAgent):
    def generate_reply(self, messages, sender, config=None):
        report = st.session_state.get("report_output", "")
        prompt = f"""You are a Critic Agent.
Review the EDA report:

{report}

Comment on clarity, accuracy, completeness, and suggest improvements."""
        return gemini_call(prompt)

class ExecutorAgent(AssistantAgent):
    def generate_reply(self, messages, sender, config=None):
        code = st.session_state.get("prep_output", "")
        prompt = f"""You are an Executor Agent.
Validate the following data preprocessing code:

{code}

- Is it runnable?
- Suggest corrections if needed."""
        return gemini_call(prompt)

# ------------------------ ADMIN AGENT ------------------------
admin_agent = UserProxyAgent(
    name="Admin",
    human_input_mode="NEVER",
    code_execution_config=False
)

# ------------------------ UI CONFIGURATION ------------------------
st.set_page_config(page_title="📊 Agentic EDA with Gemini", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 0;
        color: #3b82f6;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #6b7280;
        margin-top: 0;
    }
    .upload-section {
        border: 1px solid #e5e7eb;
        padding: 20px;
        border-radius: 10px;
        background-color: #f9fafb;
    }
    .expander-content {
        background-color: #f3f4f6;
        padding: 10px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🔍 Agentic EDA System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Powered by Gemini + Autogen Multi-Agent Collaboration</div>', unsafe_allow_html=True)
st.markdown("---")

# ------------------------ UPLOAD + PREVIEW ------------------------
with st.container():
    st.markdown("### 📁 Upload your dataset (CSV only)")
    uploaded = st.file_uploader("", type=["csv"], label_visibility="collapsed")
    if uploaded:
        df = pd.read_csv(uploaded)
        st.session_state["df"] = df

        st.subheader("📄 Dataset Preview")
        st.dataframe(df.head(), use_container_width=True)

        st.markdown("---")
        if st.button("🚀 Run Agentic EDA"):
            with st.spinner("⚙️ Initializing agents..."):
                agents = [
                    admin_agent,
                    DataPrepAgent(name="DataPrep"),
                    EDAAgent(name="EDA"),
                    ReportGeneratorAgent(name="ReportGen"),
                    CriticAgent(name="Critic"),
                    ExecutorAgent(name="Executor"),
                ]
                chat = GroupChat(agents=agents, messages=[])
                manager = GroupChatManager(groupchat=chat)

            with st.spinner("🧠 Agents analyzing your dataset..."):

                # Data Preparation Agent
                prep = agents[1].generate_reply([], "Admin")
                st.session_state["prep_output"] = prep
                with st.expander("🧹 Data Preparation Output", expanded=True):
                    st.markdown("**Python Code:**")
                    st.code(prep, language="python")

                # EDA Agent
                eda_out = agents[2].generate_reply([], "Admin")
                st.session_state["eda_output"] = eda_out
                with st.expander("📊 EDA Insights", expanded=True):
                    st.markdown(eda_out)

                # Report Generator
                report = agents[3].generate_reply([], "Admin")
                st.session_state["report_output"] = report
                with st.expander("📄 EDA Report", expanded=True):
                    st.markdown(report)

                # Critic Agent
                critique = agents[4].generate_reply([], "Admin")
                with st.expander("🧐 Critic Review", expanded=False):
                    st.markdown(critique)

                # Code Validator
                exec_feedback = agents[5].generate_reply([], "Admin")
                with st.expander("✅ Code Validation", expanded=False):
                    st.markdown(exec_feedback)

            st.success("✔️ Agentic EDA completed successfully!")

    else:
        st.info("Please upload a CSV file to begin.")
