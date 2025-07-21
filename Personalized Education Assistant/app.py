import os
import json
import requests
import re
from typing import List, Dict, Any
from dotenv import load_dotenv
import streamlit as st
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
llm_model = genai.GenerativeModel("gemini-1.5-flash")
gemini_agent_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)

# --------------------------------------
# 🧠 Helper Logic
# --------------------------------------

def fetch_resources(topic: str) -> Dict[str, Any]:
    """Fetch videos, articles, and exercises related to the topic."""
    try:
        base_url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": SERPER_API_KEY}
        
        def fetch(q):
            return requests.post(base_url, json={"q": q}, headers=headers).json().get("organic", [])[:3]
        
        result = {
            "videos": [f"{item['title']}: {item['link']}" for item in fetch(f"{topic} tutorial video")],
            "articles": [f"{item['title']}: {item['link']}" for item in fetch(f"{topic} guide article")],
            "exercises": [f"{item['title']}: {item['link']}" for item in fetch(f"{topic} practice exercises")]
        }
        return {"topic": topic, **result}

    except Exception as err:
        return {
            "topic": topic,
            "videos": [f"Error: {str(err)}"],
            "articles": [f"Error: {str(err)}"],
            "exercises": [f"Error: {str(err)}"]
        }

def create_mcqs(topic: str) -> List[Dict[str, Any]]:
    """Create multiple-choice questions using Gemini."""
    try:
        prompt = f"""
Create 3 multiple-choice questions on {topic}:
Question: ...
A) ...
B) ...
C) ...
D) ...
Answer: [A/B/C/D]
"""
        output = llm_model.generate_content(prompt).text
        blocks = output.split("Question:")[1:]
        questions = []

        for block in blocks:
            lines = [line.strip() for line in block.strip().split("\n") if line.strip()]
            if len(lines) < 5:
                continue
            q_text = lines[0]
            options = [line[3:].strip() for line in lines[1:5]]
            correct_letter = next((line.split(":")[-1].strip() for line in lines if line.startswith("Answer:")), None)
            correct = options[ord(correct_letter.upper()) - ord('A')] if correct_letter else "Unknown"
            questions.append({"question": q_text, "options": options, "answer": correct})
        
        return questions

    except Exception as err:
        return [{"question": "Error generating questions", "options": [], "answer": str(err)}]

def recommend_projects(topic: str, level: str) -> List[Dict[str, Any]]:
    """Generate practical project suggestions for a topic and skill level."""
    try:
        prompt = f"""Suggest 3 {level}-level projects on {topic}. Include:
- Project title
- Description explaining the project and why it fits the level
Format:
Project: ...
Description: ...
"""
        response = llm_model.generate_content(prompt).text
        projects = []
        for block in response.split("Project:")[1:]:
            lines = block.strip().split("\n")
            title = lines[0].strip()
            desc = next((l.split(":", 1)[-1].strip() for l in lines if l.startswith("Description:")), "")
            projects.append({"title": title, "description": desc, "level": level})
        return projects

    except Exception as err:
        return [{"title": "Error generating projects", "description": str(err), "level": level}]

# --------------------------------------
# 🧩 Crew Agents (Gemini)
# --------------------------------------

learning_curator = Agent(
    role="Learning Curator",
    goal="Research high-quality resources for self-learning",
    backstory="Expert in discovering curated video, article, and practice materials.",
    llm=gemini_agent_llm,
    verbose=True
)

quiz_master = Agent(
    role="Assessment Creator",
    goal="Formulate MCQs for conceptual understanding",
    backstory="Specialist in instructional content with deep testing strategies.",
    llm=gemini_agent_llm,
    verbose=True
)

project_mentor = Agent(
    role="Project Mentor",
    goal="Suggest hands-on learning projects",
    backstory="Veteran mentor creating realistic projects for all learner levels.",
    llm=gemini_agent_llm,
    verbose=True
)

# --------------------------------------
# 🛠️ Task Wrappers
# --------------------------------------

def build_learning_task(topic: str) -> Task:
    return Task(
        description=f"Gather top learning resources (videos, articles, exercises) about '{topic}'",
        expected_output="A structured list with 3 items in each category with links",
        agent=learning_curator
    )

def build_quiz_task(topic: str) -> Task:
    return Task(
        description=f"Generate 3 educational multiple-choice questions on '{topic}'",
        expected_output="Each question must have 4 options and 1 correct answer",
        agent=quiz_master
    )

def build_project_task(topic: str, level: str) -> Task:
    return Task(
        description=f"Suggest 3 practical projects for {level} learners on '{topic}'",
        expected_output="Project title, description, and suitability for level",
        agent=project_mentor
    )

# --------------------------------------
# 🎯 Generate Learning Path
# --------------------------------------

def build_learning_path(topic: str, level: str) -> Dict[str, Any]:
    try:
        return {
            "resources": fetch_resources(topic),
            "quizzes": create_mcqs(topic),
            "projects": recommend_projects(topic, level)
        }
    except Exception as err:
        st.error(f"Failed to build path: {err}")
        return {"resources": {}, "quizzes": [], "projects": []}

# --------------------------------------
# 🌐 Streamlit UI
# --------------------------------------

def run_ui():
    st.set_page_config("🧠 Learning Path Generator", layout="wide")
    st.title("🎓 Personalized Learning Companion")
    st.markdown("Generate learning materials, quizzes, and projects based on your topic and level.")
    
    if not GEMINI_API_KEY or not SERPER_API_KEY:
        st.error("Please set GEMINI_API_KEY and SERPER_API_KEY in your environment.")
        return
    
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/5977/5977577.png", width=100)
        st.markdown("## 🔍 Get Started")
        topic = st.text_input("📝 Topic to Learn", placeholder="e.g., Data Structures")
        level = st.selectbox("📊 Your Proficiency", ["Beginner", "Intermediate", "Advanced"])
        start = st.button("🚀 Generate Learning Path")

    if start:
        if not topic.strip():
            st.warning("Topic is required.")
            return
        
        with st.spinner("Creating personalized learning experience..."):
            result = build_learning_path(topic, level)

        st.success("✅ Learning Path Ready!")
        col1, col2, col3 = st.columns(3)
        col1.metric("🎥 Videos", len(result["resources"].get("videos", [])))
        col2.metric("📄 Articles", len(result["resources"].get("articles", [])))
        col3.metric("🚀 Projects", len(result["projects"]))

        tab1, tab2, tab3 = st.tabs(["📚 Resources", "📝 Quizzes", "💡 Projects"])

        with tab1:
            st.subheader("🎥 Videos")
            for item in result["resources"].get("videos", []):
                st.write(f"- {item}")

            st.subheader("📄 Articles")
            for item in result["resources"].get("articles", []):
                st.write(f"- {item}")

            st.subheader("💪 Exercises")
            for item in result["resources"].get("exercises", []):
                st.write(f"- {item}")

        with tab2:
            st.subheader("📝 Quiz Questions")
            for idx, q in enumerate(result["quizzes"], 1):
                st.markdown(f"**Q{idx}. {q['question']}**")
                for i, opt in enumerate(q["options"]):
                    st.write(f"  {chr(65+i)}) {opt}")
                st.success(f"✅ Correct Answer: {q['answer']}")
                st.markdown("---")

        with tab3:
            st.subheader("💡 Project Ideas")
            for i, project in enumerate(result["projects"], 1):
                st.markdown(f"### {i}. {project['title']}")
                st.write(project["description"])
                st.info(f"Level: {project['level']}")
                st.markdown("---")

    st.markdown("---")
    st.caption("Built with 💻 using Gemini AI + Serper API")

if __name__ == "__main__":
    run_ui()