import os
import time
import copy
import streamlit as st
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise EnvironmentError("GEMINI_API_KEY not found in .env file.")

import google.generativeai as genai
genai.configure(api_key=API_KEY)

CREATOR_SYSTEM_MSG = """
You are a professional AI Content Creator. You:
1. Generate markdown-based content clearly and accurately
2. Organize sections neatly
3. Avoid commentary—only return content
"""

CRITIC_SYSTEM_MSG = """
You are an expert AI Content Critic. You:
1. Evaluate markdown content based on clarity, technicality, and coherence
2. Suggest constructive revisions
3. Highlight issues in structure or completeness
"""

class GeminiAgent:
    def __init__(self, model, system_message):
        self.model = model
        self.system_message = system_message

    def generate(self, prompt):
        full_prompt = f"{self.system_message}\n\n{prompt}"
        try:
            return self.model.invoke(full_prompt).content
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def __deepcopy__(self, memo):
        return GeminiAgent(
            model=ChatGoogleGenerativeAI(model=self.model.model, google_api_key=API_KEY),
            system_message=self.system_message
        )


creator_agent = GeminiAgent(
    model=ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=API_KEY),
    system_message=CREATOR_SYSTEM_MSG
)

critic_agent = GeminiAgent(
    model=ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=API_KEY),
    system_message=CRITIC_SYSTEM_MSG
)

st.set_page_config(page_title="🧠 AI Agent Refinement", layout="wide", page_icon="🤖")

st.markdown("""
    <style>
        .section-title { font-size: 28px; font-weight: bold; color: #3b82f6; margin-bottom: 10px; }
        .agent-block { background-color: #f9fafb; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        .creator { border-left: 5px solid #3b82f6; }
        .critic { border-left: 5px solid #ef4444; }
        .final-output { background-color: #f3f4f6; padding: 20px; border-radius: 10px; border: 1px solid #d1d5db; }
        .badge { display: inline-block; background-color: #10b981; color: white; padding: 3px 10px; font-size: 12px; border-radius: 999px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='section-title'>🤖 Agentic AI Content Refinement</div>", unsafe_allow_html=True)
st.caption("Simulated collaboration between AI Creator and Critic agents using Google Gemini")

st.markdown("### 📌 Configuration")
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("💡 Enter a Topic", value="Agentic AI", placeholder="e.g. Prompt Engineering, AI Ethics")
with col2:
    num_turns = st.slider("🔄 Number of Turns", min_value=3, max_value=5, value=3)

run_simulation = st.button("🚀 Start Simulation")

if run_simulation:
    creator = AssistantAgent(
        name="Creator",
        system_message=CREATOR_SYSTEM_MSG,
        llm_config={
            "config_list": [{"model": "gemini-1.5-flash", "api_key": API_KEY}],
            "timeout": 90
        },
        human_input_mode="NEVER",
        is_termination_msg=lambda x: "TERMINATE" in x.get("content", "")
    )

    critic = AssistantAgent(
        name="Critic",
        system_message=CRITIC_SYSTEM_MSG,
        llm_config={
            "config_list": [{"model": "gemini-1.5-flash", "api_key": API_KEY}],
            "timeout": 90
        },
        human_input_mode="NEVER",
        is_termination_msg=lambda x: "TERMINATE" in x.get("content", "")
    )

    user_proxy = UserProxyAgent(name="User_Proxy", human_input_mode="NEVER", max_consecutive_auto_reply=0)

    creator_output = ""
    critic_feedback = ""
    history = []

    for turn in range(1, num_turns + 1):
        with st.status(f"🔁 Turn {turn} running...", expanded=False):
            if turn % 2 == 1:
                st.markdown(f"<div class='agent-block creator'><strong>🧠 Creator Turn {turn}</strong>", unsafe_allow_html=True)
                prompt = (
                    f"Draft comprehensive markdown content about **{topic}** covering:\n"
                    "- Key Concepts\n- Technical Foundations\n- Applications\n- Future Outlook"
                    if turn == 1 else
                    f"Revise the following markdown content based on critic feedback:\n\nFeedback:\n{critic_feedback}\n\nCurrent Content:\n{creator_output}"
                )
                st.code(prompt, language="markdown")
                creator_output = creator_agent.generate(prompt)
                st.markdown("##### 📝 Generated Content")
                st.markdown(creator_output, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                history.append((f"Creator Turn {turn}", creator_output))

            else:
                st.markdown(f"<div class='agent-block critic'><strong>🧐 Critic Turn {turn}</strong>", unsafe_allow_html=True)
                prompt = f"""
Evaluate this markdown content based on:
1. Technical Accuracy
2. Clarity & Structure
3. Suggestions for Improvement

Content:
{creator_output}
"""
                st.code(prompt, language="markdown")
                critic_feedback = critic_agent.generate(prompt)
                st.markdown("##### 📋 Critic Feedback")
                st.markdown(critic_feedback, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                history.append((f"Critic Turn {turn}", critic_feedback))

            time.sleep(1)

    st.markdown("### ✅ Final Content Output")
    st.markdown("<div class='final-output'>", unsafe_allow_html=True)
    st.markdown(f"<span class='badge'>Final Revision</span>", unsafe_allow_html=True)
    st.markdown(creator_output, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 📚 Full Interaction Log")
    for idx, (role, content) in enumerate(history, 1):
        with st.expander(f"{role}"):
            st.markdown(content, unsafe_allow_html=True)

    if st.button("🔁 Start Over"):
        st.experimental_rerun()
