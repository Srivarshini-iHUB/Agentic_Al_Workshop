from langchain.agents import Tool, initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)

def okr_tool_fn(outcomes):
    if not outcomes or not isinstance(outcomes, dict) or not outcomes.get('output'):
        return "Error: Please provide valid learning outcomes with an 'output' field"
    
    prompt = f"""
    Generate 3-5 specific, measurable OKRs based on these learning outcomes:
    {outcomes['output']}
    
    Format each OKR as:
    - Objective: [Clear learning goal]
      Key Results: 
        1. [Measurable result 1 with metric]
        2. [Measurable result 2 with metric]
        3. [Measurable result 3 with metric]
    """
    return prompt

tools = [
    Tool(
        name="RetroOKRTool",
        func=okr_tool_fn,
        description="Generates retrospective OKRs from learning outcomes"
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

def run_okr_agent(outcomes):
    try:
        if not outcomes or not isinstance(outcomes, dict) or not outcomes.get('output'):
            return {"error": "Invalid outcomes format - missing output field"}
            
        result = agent.invoke({
            "input": {
                "outcomes": outcomes['output'],
                "instructions": "Generate specific, measurable OKRs for learning development"
            }
        })
        
        return {
            "okrs": {
                "input": outcomes,
                "output": result['output'] if isinstance(result, dict) else str(result)
            }
        }
    except Exception as e:
        return {"error": f"OKR generation failed: {str(e)}"}