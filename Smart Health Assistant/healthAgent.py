import streamlit as st
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="🏥 Smart Health Assistant", layout="wide")
st.title("💡 Smart Health Assistant")

with st.sidebar:
    st.header("🔐 Configuration")
    gemini_api_key = st.text_input("🔑 Enter Gemini 1.5 Flash API Key:", type="password", placeholder="Paste your API key here...")
    st.markdown("[🌐 Get a Gemini API Key](https://aistudio.google.com/app/apikey)")
    st.caption("💬 This assistant helps calculate your BMI, generate tailored meal plans, and create a weekly workout schedule — all personalized for your health profile.")

if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "final_plan" not in st.session_state:
    st.session_state.final_plan = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_gemini_config(api_key: str, model: str = "gemini-1.5-flash"):
    return [{
        "model": model,
        "api_key": api_key,
        "api_type": "google",
        "base_url": "https://generativelanguage.googleapis.com/v1beta"
    }]

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)

# Form input section
with st.form("health_form"):
    st.subheader("🧍 Enter Your Health Details")
    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("⚖️ Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
        height = st.number_input("📏 Height (cm)", min_value=100, max_value=250, value=170)
        age = st.number_input("🎂 Age", min_value=18, max_value=100, value=30)
    with col2:
        gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])
        dietary_preference = st.selectbox("🥗 Dietary Preference", ["Veg", "Non-Veg", "Vegan"])
        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("💪 Generate Health Plan")

def init_agents(api_key, dietary_pref, age, gender):
    genai.configure(api_key=api_key)
    config_list = get_gemini_config(api_key)

    bmi_agent = AssistantAgent(
        name="BMI_Agent",
        llm_config={"config_list": config_list, "cache_seed": None},
        system_message="""🎯 You are a BMI specialist.
        1. Use the 'calculate_bmi' function with weight (kg) and height (cm)
        2. Categorize BMI: Underweight, Normal, Overweight, Obese
        3. Provide actionable health advice based on category
        Always return the exact BMI value."""
    )

    diet_agent = AssistantAgent(
        name="Diet_Planner",
        llm_config={"config_list": config_list, "cache_seed": None},
        system_message=f"""🍽️ You are a nutrition expert. Based on:
        - BMI feedback
        - Dietary preference: {dietary_pref}
        Create a detailed daily meal plan with:
        - Breakfast, Lunch, Dinner, Snacks
        - Nutritional goals and portion tips"""
    )

    workout_agent = AssistantAgent(
        name="Workout_Scheduler",
        llm_config={"config_list": config_list, "cache_seed": None},
        system_message=f"""🏋️ You are a certified fitness coach. Based on:
        - Age: {age}
        - Gender: {gender}
        - BMI and diet inputs
        Create a 7-day workout plan:
        - Include cardio, strength, flexibility
        - Duration, intensity, and rest tips"""
    )

    user_proxy = UserProxyAgent(
        name="User_Proxy",
        human_input_mode="NEVER",
        code_execution_config=False,
        llm_config={"config_list": config_list, "cache_seed": None},
        system_message="👤 You are the user proxy passing details to expert agents."
    )

    user_proxy.register_function(function_map={"calculate_bmi": calculate_bmi})

    return user_proxy, bmi_agent, diet_agent, workout_agent, config_list

if submit_btn and gemini_api_key:
    try:
        user_proxy, bmi_agent, diet_agent, workout_agent, config_list = init_agents(
            gemini_api_key, dietary_preference, age, gender
        )

        groupchat = GroupChat(
            agents=[user_proxy, bmi_agent, diet_agent, workout_agent],
            messages=[],
            max_round=6,
            speaker_selection_method="round_robin"
        )

        manager = GroupChatManager(
            groupchat=groupchat,
            llm_config={"config_list": config_list, "cache_seed": None}
        )

        initial_message = f"""
        📋 User Health Profile:
        - Weight: {weight} kg
        - Height: {height} cm
        - Age: {age}
        - Gender: {gender}
        - Dietary Preference: {dietary_preference}

        ➕ Please:
        1. BMI Agent: Calculate BMI using function
        2. Classify BMI and advise
        3. Diet Planner: Suggest personalized meals
        4. Workout Scheduler: Create a weekly routine
        """

        with st.spinner("⏳ Generating your personalized health plan..."):
            user_proxy.initiate_chat(
                manager,
                message=initial_message,
                clear_history=True
            )

            st.session_state.conversation = []
            for msg in groupchat.messages:
                if msg['role'] != 'system' and msg['content'].strip():
                    st.session_state.conversation.append((msg['name'], msg['content']))
                    if msg['name'] == "Workout_Scheduler":
                        st.session_state.final_plan = msg['content']

        st.success("✅ Health plan generated successfully!")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("📡 Please ensure your Gemini API key is valid and your internet connection is active.")


if st.session_state.conversation:
    st.divider()
    st.subheader("🔍 Agent Conversation History")

    for agent, message in st.session_state.conversation:
        with st.expander(f"🧠 {agent} says:"):
            st.markdown(message)

    st.divider()
    st.subheader("📦 Your Complete Health Plan")

    if st.session_state.final_plan:
        st.markdown(st.session_state.final_plan)
        st.download_button(
            label="⬇️ Download Health Plan",
            data=st.session_state.final_plan,
            file_name="personalized_health_plan.txt",
            mime="text/plain"
        )
    else:
        st.warning("⚠️ Workout plan not generated. Please try again.")

elif not submit_btn:
    st.divider()
    st.info("""
    ### 📝 Instructions:
    1. **Paste your Gemini API key** in the sidebar
    2. **Fill out your health profile**
    3. **Click "Generate Health Plan"**
    4. Receive a custom **BMI analysis**, **diet chart**, and **workout plan**
    """)
