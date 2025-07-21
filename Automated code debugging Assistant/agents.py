from crewai import Agent, LLM

# ----- LLM Setup -----
llm = LLM(
    api_key="AIzaSyAZtErluhP9-PX-Wd29D_QDWRG7V3xj6io",
    model="gemini/gemini-2.5-flash"
)

# ----- Agents -----
code_analyzer = Agent(
    role="Python Static Analyzer",
    goal="Find issues in Python code WITHOUT executing it",
    backstory="Expert in static code analysis using AST parsing.",
    llm=llm,
    verbose=True
)

code_corrector = Agent(
    role="Python Code Fixer",
    goal="Fix issues while keeping original functionality",
    backstory="Specializes in clean, PEP 8 compliant fixes.",
    llm=llm,
    verbose=True
)

manager = Agent(
    role="Code Review Manager",
    goal="Ensure smooth analysis & correction",
    backstory="Coordinates the review process.",
    llm=llm,
    verbose=True
)
