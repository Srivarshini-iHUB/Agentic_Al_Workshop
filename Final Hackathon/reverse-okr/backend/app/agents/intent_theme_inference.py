from langchain.agents import Tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)

def intent_tool_fn(activities):
    if not activities or not isinstance(activities, list):
        return "Error: Invalid input - expected list of activities"
    return f"Infer themes and intent from these activities: {activities}"

tools = [
    Tool(
        name="ThemeIntentTool",
        func=intent_tool_fn,
        description="Infers learning themes and intent from activity JSON"
    )
]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

def run_intent_agent(activities):
    try:
        result = agent.invoke({"input": activities})
        return {"themes": result}
    except Exception as e:
        return {"error": str(e)}