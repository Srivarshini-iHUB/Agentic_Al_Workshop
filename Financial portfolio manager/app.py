import os
import json
import streamlit as st
from dotenv import load_dotenv
from autogen import AssistantAgent, UserProxyAgent

load_dotenv()
GOOGLE_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_KEY:
    raise ValueError("Missing Gemini API key in environment variables.")

gemini_settings = [{
    "model": "gemini-2.5-flash",
    "api_key": GOOGLE_KEY,
    "api_type": "google"
}]

st.set_page_config(page_title="💼 Portfolio Planner", layout="centered")
st.title("📈 Financial Portfolio Planner")
st.markdown("Get a personalized investment strategy powered by AI.")

with st.form("portfolio_form"):
    income = st.text_input("Total Annual Income (₹)", placeholder="1200000")
    user_age = st.number_input("Current Age", 18, 100)
    annual_expenses = st.text_input("Annual Expenses (₹)", placeholder="500000")
    life_goals = st.text_area("Your Financial Goals", placeholder="e.g., Retire by 60, Buy a home in 5 years")
    risk_level = st.selectbox("Choose Risk Appetite", ["Conservative", "Moderate", "Aggressive"])

    st.divider()
    st.subheader("📊 Asset Allocation Details")
    mf_input = st.text_area("Mutual Funds (Name - Type - Value)", placeholder="Mirae Large Cap - Equity - ₹1.5L")
    stock_input = st.text_area("Stocks (Name - Qty - Buy Price)", placeholder="TCS - 20 shares - ₹3200")
    realty_input = st.text_area("Real Estate Holdings", placeholder="Plot - Pune - ₹15L")
    fd_amount = st.text_input("Fixed Deposits Total (₹)", placeholder="500000")

    form_submit = st.form_submit_button("📝 Generate Investment Plan")

agent_analyst = AssistantAgent(
    name="InvestmentAnalyst",
    llm_config={"config_list": gemini_settings},
    system_message="""
    Assess the financial portfolio provided and determine a suitable investment approach.
    Respond in JSON only: {"strategy": "Growth" or "Value", "reason": "brief summary"}
    """
)

agent_growth = AssistantAgent(
    name="GrowthAdvisor",
    llm_config={"config_list": gemini_settings},
    system_message="""
    Recommend high-return investment options like tech equities, mid-cap funds, or digital assets.
    Respond as: {"recommendations": [...], "rationale": "summary"}
    """
)

agent_value = AssistantAgent(
    name="ValueAdvisor",
    llm_config={"config_list": gemini_settings},
    system_message="""
    Recommend stable options such as FDs, PPFs, blue-chip stocks, or low-risk debt instruments.
    Respond as: {"recommendations": [...], "rationale": "summary"}
    """
)

agent_reporter = AssistantAgent(
    name="ReportCompiler",
    llm_config={"config_list": gemini_settings},
    system_message="""
    Construct a comprehensive financial analysis report including:
    1. Summary of current portfolio
    2. Strategy chosen
    3. AI-generated investment suggestions
    4. Step-by-step implementation plan
    5. Risk outlook
    Output in Markdown format. End with 'TERMINATE'
    """
)

agent_user = UserProxyAgent(
    name="ClientAgent",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    code_execution_config=False,
    is_termination_msg=lambda msg: "TERMINATE" in msg.get("content", "")
)

def get_strategy_from_json(content):
    try:
        parsed = json.loads(content.strip())
        return parsed.get("strategy", "Growth")
    except json.JSONDecodeError:
        return "Growth"

def run_financial_flow():
    profile = f"""
Client Details:
- Age: {user_age}
- Salary: ₹{income}
- Yearly Expenses: ₹{annual_expenses}
- Risk Profile: {risk_level}
- Goals: {life_goals}

Assets:
- Mutual Funds: {mf_input or 'N/A'}
- Stocks: {stock_input or 'N/A'}
- Real Estate: {realty_input or 'N/A'}
- Fixed Deposits: ₹{fd_amount or '0'}
"""

    # Step 1 - Portfolio Review
    analysis = agent_user.initiate_chat(agent_analyst, message=profile, summary_method="last_msg", silent=True)
    analysis_content = analysis.chat_history[-1]["content"]
    investment_strategy = get_strategy_from_json(analysis_content)

    # Step 2 - Recommendations
    suggestion_agent = agent_growth if investment_strategy == "Growth" else agent_value
    tips = agent_user.initiate_chat(
        suggestion_agent,
        message=f"{profile}\nStrategy Chosen: {investment_strategy}",
        summary_method="last_msg",
        silent=True
    )
    recommendation_text = tips.chat_history[-1]["content"]

    # Step 3 - Compile Full Report
    final_report = agent_user.initiate_chat(
        agent_reporter,
        message=f"""
Client Inputs:
{profile}

Analysis Summary:
{analysis_content}

AI Suggestions:
{recommendation_text}

Prepare a formatted report with 5 sections as instructed earlier.
""",
        summary_method="last_msg",
        silent=True
    )

    final_content = final_report.chat_history[-1]["content"]
    return final_content.split("TERMINATE")[0].strip() if "TERMINATE" in final_content else final_content

if form_submit:
    with st.spinner("🔍 Analyzing your financial profile..."):
        try:
            output = run_financial_flow()
            st.subheader("📘 Your Investment Blueprint")
            st.markdown(output)
        except Exception as err:
            st.error(f"⚠️ Failed to generate report: {str(err)}")
            st.info("Please review your input fields and try again.")
