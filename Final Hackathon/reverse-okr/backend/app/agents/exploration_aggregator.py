from langchain.agents import Tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

def aggregate_tool_fn(logs):
    return f"Aggregate these logs into JSON structure with activity type, title, and metadata: {logs}"

tools = [
    Tool(
        name="AggregatorTool",
        func=lambda x: aggregate_tool_fn(x),
        description="Aggregates exploration logs into structured activity JSON"
    )
]

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

def run_exploration_agent(logs):
    result = agent.invoke(logs)
    return {"activities": result}