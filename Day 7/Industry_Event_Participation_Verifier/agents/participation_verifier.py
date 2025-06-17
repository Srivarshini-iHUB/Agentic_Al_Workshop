from google.generativeai import GenerativeModel
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = GenerativeModel("gemini-1.5-flash")

def verify_participation(evidence_text):
    prompt = f"Based on the following evidence, did the user actually attend and participate in the industry event?\n\n{evidence_text}\n\nReturn just Yes or No."
    result = model.generate_content(prompt).text.strip().lower()
    return "yes" in result
