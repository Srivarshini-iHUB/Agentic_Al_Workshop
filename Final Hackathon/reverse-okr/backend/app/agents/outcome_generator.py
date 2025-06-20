from langchain.agents import Tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)

def outcome_tool_fn(knowledge_graph):
    if not knowledge_graph or not isinstance(knowledge_graph, dict):
        return "Error: Invalid input - expected knowledge graph dict"
    
    prompt = f"""
    Suggest 3-5 actionable learning outcomes based on this knowledge graph:
    {knowledge_graph}
    
    Format each outcome as:
    - [Specific skill or knowledge area to develop]
    - [Suggested activities or resources]
    - [Expected measurable improvement]
    """
    return prompt

tools = [
    Tool(
        name="OutcomeSuggesterTool",
        func=outcome_tool_fn,
        description="Suggests actionable learning outcomes from graph"
    )
]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)

def run_outcome_agent(knowledge_graph):
    try:
        result = agent.invoke({
            "input": {
                "knowledge_graph": knowledge_graph,
                "instructions": "Generate specific, actionable learning outcomes"
            }
        })
        
        return {
            "outcomes": {
                "input": knowledge_graph,
                "output": result['output'] if isinstance(result, dict) else str(result)
            }
        }
    except Exception as e:
        return {"error": str(e)}