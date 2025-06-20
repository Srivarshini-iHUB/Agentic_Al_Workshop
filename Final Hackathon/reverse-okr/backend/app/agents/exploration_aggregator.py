from langchain.agents import Tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GOOGLE_API_KEY
from helper.extract_youtube_metadata import extract_video_metadata


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)

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
    enriched_logs = []
    for log in logs:
        if isinstance(log, str) and "youtube.com" in log:
            enriched_logs.append(extract_video_metadata(log))
        else:
            enriched_logs.append({
                "activity_type": "text",
                "title": log[:50] + "...",
                "metadata": {"raw": log}
            })

    result = agent.invoke({"input": enriched_logs})
    return {"activities": result}
