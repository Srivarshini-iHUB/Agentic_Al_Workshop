import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

st.set_page_config(
    page_title="🚛 AI-Powered Logistics Planner",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.header-box {
    background: linear-gradient(90deg, #4b6cb7, #182848);
    color: white;
    padding: 2rem;
    border-radius: 1rem;
    text-align: center;
    margin-bottom: 2rem;
}

.input-box {
    background: linear-gradient(to right, #ff9966, #ff5e62);
    padding: 1.5rem;
    border-radius: 1rem;
    margin-bottom: 2rem;
    color: white;
    font-weight: 500;
    text-align: center;
}

.result-box {
    background: #f7f9fc;
    border: 1px solid #ddd;
    border-radius: 1rem;
    padding: 1.5rem;
    margin-top: 1.5rem;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <h1>🚛 AI Logistics Optimizer</h1>
    <p>Let AI analyze and streamline your supply chain operations</p>
</div>
""", unsafe_allow_html=True)

with st.form("optimizer_form"):
    st.markdown('<div class="input-box">📦 Enter products separated by commas to analyze logistics and optimize them</div>', unsafe_allow_html=True)
    product_input = st.text_input("Products", placeholder="E.g., TV, Headphones, Air Conditioner")
    submitted = st.form_submit_button("🔎 Analyze Logistics")

if submitted:
    if not GOOGLE_API_KEY:
        st.error("🚫 Missing Google API Key. Please check your `.env` file or environment settings.")
        st.stop()

    products = [p.strip() for p in product_input.split(",") if p.strip()]
    if not products:
        st.warning("⚠️ Please enter at least one product.")
        st.stop()

    with st.spinner("🧠 Running AI Agents to analyze and optimize..."):

        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0.3
            )

            logistics_agent = Agent(
                role="Supply Chain Analyst",
                goal="Identify weak points in shipping and inventory turnover for various products.",
                backstory="A senior analyst trained in root-cause logistics analysis for enterprise supply chains.",
                llm=llm,
                verbose=True,
                tools=[],
            )

            strategy_agent = Agent(
                role="Logistics Optimization Expert",
                goal="Develop smart strategies to enhance delivery speed, lower cost, and minimize inventory issues.",
                backstory="A logistics strategist renowned for reducing delivery cycles using AI modeling.",
                llm=llm,
                verbose=True,
                tools=[],
            )

            analysis_task = Task(
                description=f"Study logistics for these products: {products}. Spot inefficiencies in delivery, routing, or inventory usage.",
                expected_output="Detailed findings with pain points and inefficiency insights.",
                agent=logistics_agent
            )

            strategy_task = Task(
                description="Create a logistics plan to improve speed and cut delivery cost using insights from the logistics analyst.",
                expected_output="A practical logistics optimization plan with clear, actionable items.",
                agent=strategy_agent
            )

            crew = Crew(
                agents=[logistics_agent, strategy_agent],
                tasks=[analysis_task, strategy_task],
                verbose=True
            )

            final_result = crew.kickoff()

            st.success("✅ Analysis Complete!")
            st.markdown("### 📋 AI-Generated Optimization Strategy")
            st.markdown(f"<div class='result-box'>{final_result}</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error("💥 Something went wrong while running the AI agents.")
            st.code(str(e), language="bash")
