import streamlit as st
import time
import google.generativeai as genai
from autogen import AssistantAgent, UserProxyAgent
from langchain_google_genai import ChatGoogleGenerativeAI
import copy
import os

# -------------------- CONFIGURATION --------------------
api_key = "AIzaSyDG-0xIaprzdT70VTf-LnMt62_s-F8SJqA"
genai.configure(api_key=api_key)

CREATOR_SYSTEM_MESSAGE = """
You are a Content Creator Agent specializing in Generative AI. Your role is to:
1. Draft clear, concise, and technically accurate content
2. Revise content based on constructive feedback
3. Structure output in markdown format
4. Focus exclusively on content creation (no commentary)
"""

CRITIC_SYSTEM_MESSAGE = """
You are a Content Critic Agent evaluating Generative AI content. Your role is to:
1. Analyze technical accuracy and language clarity
2. Provide specific, constructive feedback
3. Identify both strengths and areas for improvement
4. Maintain professional, objective tone
"""

# -------------------- AGENT WRAPPER --------------------
class GeminiAgent:
    def __init__(self, model, system_message):
        self.model = model
        self.system_message = system_message

    def generate(self, prompt):
        full_prompt = self.system_message + "\n\n" + prompt
        try:
            response = self.model.invoke(full_prompt)
            return response.content
        except Exception as e:
            return f"Error: {str(e)}"

    def __deepcopy__(self, memo):
        return GeminiAgent(
            model=ChatGoogleGenerativeAI(model=self.model.model, google_api_key=api_key),
            system_message=self.system_message
        )

creator_model = GeminiAgent(
    model=ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key),
    system_message=CREATOR_SYSTEM_MESSAGE
)

critic_model = GeminiAgent(
    model=ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key),
    system_message=CRITIC_SYSTEM_MESSAGE
)

# -------------------- STREAMLIT UI --------------------
st.set_page_config(page_title="🤖 Agentic Content Refinement", layout="wide")

st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #3b82f6;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #6b7280;
            margin-bottom: 20px;
        }
        .turn-title {
            margin-top: 20px;
            font-size: 20px;
            font-weight: 600;
            color: #10b981;
        }
        .final-section {
            background-color: #f3f4f6;
            padding: 15px;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🤖 Agentic AI Content Refinement</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Simulated Collaboration Between Creator & Critic Agents</div>', unsafe_allow_html=True)
st.markdown("---")

topic = st.text_input("🎯 Discussion Topic", "Agentic AI")
turns = st.slider("🔁 Conversation Turns", 3, 5, 3)
generate_btn = st.button("🚀 Start Simulation")

if generate_btn:
    creator = AssistantAgent(
        name="Creator",
        system_message=CREATOR_SYSTEM_MESSAGE,
        llm_config={
            "config_list": [
                {
                    "model": "gemini-1.5-flash",
                    "api_key": api_key,
                    "base_url": "https://generativelanguage.googleapis.com/v1beta/models/"
                }
            ],
            "timeout": 120
        },
        human_input_mode="NEVER",
        is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    )

    critic = AssistantAgent(
        name="Critic",
        system_message=CRITIC_SYSTEM_MESSAGE,
        llm_config={
            "config_list": [
                {
                    "model": "gemini-1.5-flash",
                    "api_key": api_key,
                    "base_url": "https://generativelanguage.googleapis.com/v1beta/models/"
                }
            ],
            "timeout": 120
        },
        human_input_mode="NEVER",
        is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    )

    user_proxy = UserProxyAgent(
        name="User_Proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
        code_execution_config=False,
    )

    conversation_history = []
    creator_output = ""
    critic_feedback = ""

    for turn in range(1, turns + 1):
        with st.status(f"💬 Turn {turn} in progress...", expanded=False):
            # Creator Turn
            if turn % 2 == 1:
                st.markdown(f'<div class="turn-title">✍️ Turn {turn}: Content Creator</div>', unsafe_allow_html=True)
                if turn == 1:
                    prompt = f"Draft comprehensive content about **{topic}** in markdown format covering:\n- Key concepts\n- Technical foundations\n- Real-world applications\n- Future implications"
                else:
                    prompt = f"Revise this content based on the critic's feedback:\n\n{critic_feedback}\n\nCurrent content:\n{creator_output}\n\nProvide improved markdown content:"

                st.markdown("**📝 Prompt:**")
                st.code(prompt, language="markdown")

                creator_output = creator_model.generate(prompt)

                st.markdown("**🧠 Generated Content:**")
                st.markdown(creator_output, unsafe_allow_html=True)
                conversation_history.append(("Creator", creator_output))

            # Critic Turn
            else:
                st.markdown(f'<div class="turn-title">🧐 Turn {turn}: Content Critic</div>', unsafe_allow_html=True)
                prompt = f"""Evaluate this content based on:\n
1. Technical accuracy\n
2. Clarity of explanations\n
3. Depth of coverage\n
4. Suggestions for improvement\n
\nContent:\n{creator_output}"""

                st.markdown("**📋 Prompt:**")
                st.code(prompt, language="markdown")

                critic_feedback = critic_model.generate(prompt)

                st.markdown("**📣 Feedback:**")
                st.markdown(critic_feedback, unsafe_allow_html=True)
                conversation_history.append(("Critic", critic_feedback))

            time.sleep(1)

    # Final Output
    st.markdown("---")
    st.markdown("## ✅ Final Creator Output")
    st.markdown('<div class="final-section">', unsafe_allow_html=True)
    st.markdown(creator_output, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Full Trace
    st.markdown("---")
    st.markdown("## 🗂️ Full Conversation History")
    for i, (role, content) in enumerate(conversation_history, 1):
        with st.expander(f"{role} - Turn {i}"):
            st.markdown(content, unsafe_allow_html=True)
