from google.generativeai import GenerativeModel
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = GenerativeModel("gemini-1.5-flash")

def extract_learning(notes):
    prompt = f"Summarize the key learning outcomes, technical terms, and insights from the following:\n\n{notes}"
    return model.generate_content(prompt).text.strip()
