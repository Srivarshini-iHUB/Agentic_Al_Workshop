from langchain.agents import Tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

def kg_tool_fn(themes):
    if not themes or not isinstance(themes, (list, dict)):
        return "Error: Invalid input - expected themes list or dict"
    return f"Build a knowledge graph mapping themes to concepts and skills: {themes}"

tools = [
    Tool(
        name="KGBuilderTool",
        func=kg_tool_fn,
        description="Maps themes to knowledge graph nodes and links"
    )
]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

def run_kg_agent(themes):
    try:
        result = agent.invoke({"input": themes})
        return {"knowledge_graph": result}
    except Exception as e:
        return {"error": str(e)}