from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from agents.weather_tool import get_weather_tool
from agents.attractions_tool import get_attractions_tool

import os
from dotenv import load_dotenv

load_dotenv()

def initialize_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.7,
    )

    tools = [get_weather_tool(), get_attractions_tool()]

    # ✅ Add agent_scratchpad to support internal tool reasoning
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful travel assistant. Answer clearly and concisely."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),  # ✅ This line fixes the error
    ])

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )

    return agent_executor
