# 🐍 AI-Powered Python Code Reviewer

An AI-powered tool that performs **static code analysis** and **auto-corrects Python code** — without executing it. Built using:

- 🧠 CrewAI agents (Analyzer, Fixer, Manager)
- 🤖 Google Gemini LLM (via LangChain)
- 🖥️ Streamlit UI for easy interaction

---

## ✨ Key Features

- 🔍 Analyzes Python code using the `ast` module for static analysis
- ⚠️ Detects issues like:
  - `print()` usage in production (encourages use of logging)
  - Bare `except:` blocks (recommends specifying exception types)
- 🛠️ Automatically fixes issues using Gemini LLM
- 💬 Provides natural language explanations
- 🔒 Static analysis only — **no code execution**

---

## 🧠 Agent Workflow

1. **Analyzer Agent**  
   Parses the code using AST and identifies potential issues, such as print statements and bare except blocks.

2. **Fixer Agent**  
   Suggests clean, PEP8-compliant corrections using Gemini while preserving original logic.

3. **Manager Agent**  
   Coordinates the review and fix tasks to ensure a smooth workflow.

---

## 🛠️ Installation Guide

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

1. Clone the repository.
2. Install dependencies using the installation guide above.
3. Run the app:

```bash
streamlit run app.py
```

4. Open the displayed URL in your browser.
5. Paste your Python code into the input box.
6. Click "Analyze & Fix Code" to get analysis and corrections.

---

## 🗂️ Project Structure

- `app.py`: Streamlit UI and main app logic.
- `utils.py`: Static analysis utility functions using AST parsing.
- `agents.py`: LLM and CrewAI agent setup.

---





