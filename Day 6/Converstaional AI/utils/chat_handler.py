# utils/chat_handler.py
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(history=[])

def ask_gemini_with_context(user_question, search_snippets):
    prompt = f"""
You are a business AI helping clothing store owners gain competitive insights.

Here are real-time internet results about the user's query:
---
{search_snippets}
---

Now respond to the user's question:
{user_question}

Provide clear business strategies, insights, and suggestions.
"""
    response = chat.send_message(prompt)
    return response.text
