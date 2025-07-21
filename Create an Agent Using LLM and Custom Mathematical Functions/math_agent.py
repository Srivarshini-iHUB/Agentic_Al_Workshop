from langgraph.graph import StateGraph, END
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import TypedDict, List, Optional, Annotated, Union
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import operator
import streamlit as st
import time
from datetime import datetime

load_dotenv()
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        google_api_key=os.getenv("GOOGLE_API_KEY"), 
        temperature=0
    )
except Exception as e:
    st.error(f"Failed to initialize LLM: {str(e)}")

st.set_page_config(
    page_title="AI Math & Q&A Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
        font-weight: 300;
    }
    
    .chat-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        min-height: 600px;
        border: 1px solid #e2e8f0;
    }
    
    .message-container {
        margin: 1.5rem 0;
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 25px 25px 5px 25px;
        margin-left: 20%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        position: relative;
    }
    
    .user-message::before {
        content: '👤';
        position: absolute;
        top: -10px;
        right: 15px;
        font-size: 1.5rem;
        background: white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .agent-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 25px 25px 25px 5px;
        margin-right: 20%;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
        position: relative;
    }
    
    .agent-message::before {
        content: '🤖';
        position: absolute;
        top: -10px;
        left: 15px;
        font-size: 1.5rem;
        background: white;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .message-timestamp {
        font-size: 0.8rem;
        opacity: 0.7;
        margin-top: 0.5rem;
        text-align: right;
    }
    
    .tool-usage-badge {
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-top: 0.5rem;
        display: inline-block;
        backdrop-filter: blur(10px);
    }
    
    .input-section {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-top: 2rem;
        box-shadow: 0 8px 32px rgba(132, 250, 176, 0.2);
    }
    
    .input-section h3 {
        color: white;
        font-weight: 600;
        text-align: center;
        margin-bottom: 1.5rem;
        font-size: 1.4rem;
    }
    
    .sidebar-section {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .tool-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-left: 3px solid #38b2ac;
    }
    
    .tool-name {
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.3rem;
    }
    
    .tool-description {
        font-size: 0.9rem;
        color: #718096;
        line-height: 1.4;
    }
    
    .stats-section {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: #8b4513;
    }
    
    .stat-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(139, 69, 19, 0.2);
    }
    
    .stat-item:last-child {
        border-bottom: none;
    }
    
    .processing-indicator {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem;
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        border-radius: 15px;
        margin: 1rem 0;
        color: #2d3436;
        font-weight: 500;
    }
    
    .loading-dots {
        display: inline-block;
        margin-left: 0.5rem;
    }
    
    .loading-dots::after {
        content: '';
        animation: dots 2s infinite;
    }
    
    @keyframes dots {
        0%, 20% { content: ''; }
        40% { content: '.'; }
        60% { content: '..'; }
        80%, 100% { content: '...'; }
    }
    
    .clear-button {
        background: linear-gradient(135deg, #ff7675 0%, #fd79a8 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
        transition: transform 0.2s ease;
        box-shadow: 0 4px 15px rgba(255, 118, 117, 0.3);
    }
    
    .clear-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 118, 117, 0.4);
    }
    
    .welcome-message {
        text-align: center;
        padding: 3rem 2rem;
        color: #718096;
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
        border-radius: 20px;
        margin: 2rem 0;
    }
    
    .welcome-message h3 {
        font-size: 1.8rem;
        margin-bottom: 1rem;
        color: #667eea;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border-top: 4px solid #667eea;
        transition: transform 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <div class="main-header">
        <h1> AI Math & Q&A Assistant</h1>
        <p>Powered by LangGraph & Gemini - Ask questions or solve math problems!</p>
    </div>
""", unsafe_allow_html=True)

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    user_input: str
    agent_outcome: Optional[Union[BaseMessage, List[tuple]]]
    intermediate_steps: List
@tool
def plus(a: float, b: float) -> float:
    """Add two numbers together. Use for addition problems and sum calculations."""
    return a + b

@tool
def sub(a: float, b: float) -> float:
    """Subtract b from a. Use for subtraction problems and difference calculations."""
    return a - b

@tool
def mul(a: float, b: float) -> float:
    """Multiply two numbers. Use for multiplication problems and product calculations."""
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Divide a by b. Use for division problems and ratio calculations. Handles zero division."""
    if b == 0:
        return "Error: Cannot divide by zero"
    return a / b

tools = [plus, sub, mul, divide]

system_prompt = """You are an intelligent assistant that excels at:
- Answering general knowledge questions with accurate, detailed responses
- Performing mathematical calculations using specialized tools
- Providing clear explanations for complex topics
- Helping users understand concepts step by step

For math operations, always use the appropriate tools for accuracy.
For general questions, provide comprehensive and helpful responses.
Always be friendly, professional, and clear in your communication.

When using math tools, explain your process and show the calculation steps."""
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]),
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'tool_usage' not in st.session_state:
    st.session_state.tool_usage = {'plus': 0, 'sub': 0, 'mul': 0, 'divide': 0}
with st.sidebar:
    st.markdown("## 🔧 Available Tools")
    
    tool_descriptions = {
        'plus': (' Addition', 'Adds two numbers together'),
        'sub': (' Subtraction', 'Subtracts second number from first'),
        'mul': (' Multiplication', 'Multiplies two numbers'),
        'divide': ('Division', 'Divides first number by second')
    }
    
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    for tool_name, (icon_name, description) in tool_descriptions.items():
        st.markdown(f"""
            <div class="tool-card">
                <div class="tool-name">{icon_name}</div>
                <div class="tool-description">{description}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("## Session Stats")
    st.markdown(f"""
        <div class="stats-section">
            <div class="stat-item">
                <span> Messages:</span>
                <span>{st.session_state.message_count}</span>
            </div>
            <div class="stat-item">
                <span>Tool Uses:</span>
                <span>{sum(st.session_state.tool_usage.values())}</span>
            </div>
            <div class="stat-item">
                <span> Additions:</span>
                <span>{st.session_state.tool_usage['plus']}</span>
            </div>
            <div class="stat-item">
                <span> Subtractions:</span>
                <span>{st.session_state.tool_usage['sub']}</span>
            </div>
            <div class="stat-item">
                <span> Multiplications:</span>
                <span>{st.session_state.tool_usage['mul']}</span>
            </div>
            <div class="stat-item">
                <span> Divisions:</span>
                <span>{st.session_state.tool_usage['divide']}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.session_state.message_count = 0
        st.session_state.tool_usage = {'plus': 0, 'sub': 0, 'mul': 0, 'divide': 0}
        st.rerun()

def agent_node(state: AgentState):
    """Process user input through the agent"""
    try:
        result = agent_executor.invoke({
            "input": state["user_input"],
            "chat_history": state["messages"]
        })
   
        if "intermediate_steps" in result:
            for step in result.get("intermediate_steps", []):
                if len(step) >= 1 and hasattr(step[0], 'tool'):
                    tool_name = step[0].tool
                    if tool_name in st.session_state.tool_usage:
                        st.session_state.tool_usage[tool_name] += 1
        
        return {
            "messages": [AIMessage(content=result["output"])],
            "agent_outcome": result["output"]
        }
    except Exception as e:
        error_msg = f"I encountered an error: {str(e)}. Please try rephrasing your question."
        return {
            "messages": [AIMessage(content=error_msg)],
            "agent_outcome": error_msg
        }

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)
app = workflow.compile()

def run_agent(query: str, chat_history: List[BaseMessage] = []) -> str:
    """Execute the agent with a user query using LangGraph (same logic)"""
    try:
        inputs = {
            "messages": chat_history,
            "user_input": query,
            "agent_outcome": None,
            "intermediate_steps": []
        }
        response = app.invoke(inputs)
        return response["agent_outcome"]
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}. Please try again."

def detect_tool_usage(response: str) -> List[str]:
    """Detect which tools were likely used based on response content"""
    tools_used = []
    if any(word in response.lower() for word in ['add', 'sum', 'plus', '+']):
        tools_used.append('Addition')
    if any(word in response.lower() for word in ['subtract', 'minus', 'difference', '-']):
        tools_used.append(' Subtraction') 
    if any(word in response.lower() for word in ['multiply', 'times', 'product', '×', '*']):
        tools_used.append(' Multiplication')
    if any(word in response.lower() for word in ['divide', 'division', 'quotient', '÷', '/']):
        tools_used.append(' Division')
    return tools_used


st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if not st.session_state.chat_history:
    st.markdown("""
        <div class="welcome-message">
            <h3>Welcome to Your AI Assistant! 🎉</h3>
            <p>I can help you with math calculations and answer your questions.</p>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">🧮</div>
                    <div class="feature-title">Math Calculations</div>
                    <p>Addition, subtraction, multiplication, division</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">❓</div>
                    <div class="feature-title">General Q&A</div>
                    <p>Ask me anything - science, history, technology</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🚀</div>
                    <div class="feature-title">LangGraph Powered</div>
                    <p>Advanced AI workflow with tool integration</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">💡</div>
                    <div class="feature-title">Step-by-Step</div>
                    <p>Clear explanations and reasoning</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


for i, message in enumerate(st.session_state.chat_history):
    timestamp = datetime.now().strftime("%H:%M")
    
    st.markdown('<div class="message-container">', unsafe_allow_html=True)
    
    if message["role"] == "user":
        st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {message["content"]}
                <div class="message-timestamp">{timestamp}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        tools_used = detect_tool_usage(message["content"])
        tools_badge = ""
        if tools_used:
            tools_badge = f'<div class="tool-usage-badge">Tools: {", ".join(tools_used)}</div>'
        
        st.markdown(f"""
            <div class="agent-message">
                <strong>AI Assistant:</strong> {message["content"]}
                {tools_badge}
                <div class="message-timestamp">{timestamp}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


st.markdown("""
    <div class="input-section">
        <h3>💬 Ask me anything or solve math problems!</h3>
    </div>
""", unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "",
            placeholder="e.g., 'What is 15 * 23?' or 'Explain photosynthesis'",
            key="user_input",
            help="Type your question or math problem here"
        )
    
    with col2:
        submit_button = st.form_submit_button("Send ", use_container_width=True)

if submit_button and user_input.strip():
    st.session_state.chat_history.append({
        "role": "user", 
        "content": user_input
    })
    st.session_state.message_count += 1
    with st.empty():
        st.markdown("""
            <div class="processing-indicator">
                🤖 AI is thinking<span class="loading-dots"></span>
            </div>
        """, unsafe_allow_html=True)
        messages = []
        for msg in st.session_state.chat_history[:-1]:  
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))

        response = run_agent(user_input, messages)
        
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": str(response)
        })
        st.session_state.message_count += 1

    st.rerun()

st.markdown("---")
st.markdown("## 💡 Example Queries")

example_cols = st.columns(2)

with example_cols[0]:
    st.markdown("###  Math Examples")
    if st.button("What is 156 + 289?", key="math1"):
        st.session_state.chat_history.extend([
            {"role": "user", "content": "What is 156 + 289?"},
        ])
        st.rerun()
    
    if st.button("Calculate 25 × 47", key="math2"):
        st.session_state.chat_history.extend([
            {"role": "user", "content": "Calculate 25 × 47"},
        ])
        st.rerun()

with example_cols[1]:
    st.markdown("###  Q&A Examples")
    if st.button("Explain how photosynthesis works", key="qa1"):
        st.session_state.chat_history.extend([
            {"role": "user", "content": "Explain how photosynthesis works"},
        ])
        st.rerun()
    
    if st.button("What is machine learning?", key="qa2"):
        st.session_state.chat_history.extend([
            {"role": "user", "content": "What is machine learning?"},
        ])
        st.rerun()

