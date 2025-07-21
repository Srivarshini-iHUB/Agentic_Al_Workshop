# agents.py
from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    api_key=os.getenv("GEMINI_API_KEY"), 
    model="gemini/gemini-2.5-flash"
)

code_analyzer = Agent(
    role="🕵️‍♂️ Python Static Analyzer",
    goal="Find issues in Python code WITHOUT executing it",
    backstory="Expert in static code analysis using AST parsing, linters, and static inspection techniques.",
    llm=llm,
    verbose=True
)

code_corrector = Agent(
    role="🛠️ Python Code Fixer",
    goal="Fix issues while keeping original functionality intact",
    backstory="Clean coder focused on preserving logic while ensuring code is elegant and PEP 8 compliant.",
    llm=llm,
    verbose=True
)

manager = Agent(
    role="🧠 Code Review Manager",
    goal="Oversee analysis and corrections in a smooth workflow",
    backstory="Experienced reviewer coordinating all agents during code review.",
    llm=llm,
    verbose=True
)
