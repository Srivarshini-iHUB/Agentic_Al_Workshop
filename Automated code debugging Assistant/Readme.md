# 🐍 AI-Powered Python Code Reviewer

An AI-powered tool that performs **static code analysis** and **auto-corrects Python code** — without executing it. Built using:

- 🧠 CrewAI agents (Analyzer, Fixer, Manager)
- 🤖 Google Gemini LLM (via LangChain)
- 🖥️ Streamlit UI for easy interaction

---

## ✨ Key Features

- 🔍 Analyzes Python code using the `ast` module
- ⚠️ Detects issues like:
  - `print()` usage in production
  - Bare `except:` blocks
- 🛠️ Automatically fixes issues using Gemini LLM
- 💬 Provides natural language explanations
- 🔒 Static analysis only — **no code execution**

---

## 🧠 Agent Workflow

1. **Analyzer Agent**  
   Parses the code using AST and identifies potential issues.

2. **Fixer Agent**  
   Suggests clean, PEP8-compliant corrections using Gemini.

3. **Manager Agent**  
   Coordinates the review and fix tasks.

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
- `utils.py`: Static analysis utility functions.
- `agents.py`: LLM and CrewAI agent setup.

---

## 💡 Notes

- Ensure your Google API key is set in the environment variable `GOOGLE_API_KEY` (already set in `app.py` for convenience).
- This tool performs static analysis only; it does not execute your code.
pip install -r requirements.txt




