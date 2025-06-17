import fitz  # PyMuPDF
from PIL import Image
from google.generativeai import GenerativeModel
from dotenv import load_dotenv
import os
import tempfile
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

text_model = GenerativeModel("gemini-1.5-flash")
vision_model = GenerativeModel("gemini-1.5-flash")

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "".join([page.get_text() for page in doc])

def extract_text_from_image(file):
    image = Image.open(file)
    prompt = "Extract the event name, date, location, and ticket or registration info from this image."
    response = vision_model.generate_content([prompt, image])
    return response.text

def parse_event_info(raw_text):
    prompt = f"""
    From the following text, extract and return these fields in JSON:
    - event_name
    - event_date
    - location
    - ticket_number or registration_id (if present)

    Text:
    {raw_text}
    """
    return text_model.generate_content(prompt).text

def extract_evidence(files):
    all_raw_text = ""
    for file in files:
        filename = file.name.lower()
        if filename.endswith(".pdf"):
            all_raw_text += extract_text_from_pdf(file) + "\n"
        elif filename.endswith((".jpg", ".jpeg", ".png")):
            all_raw_text += extract_text_from_image(file) + "\n"
        else:
            all_raw_text += file.read().decode("utf-8") + "\n"

    parsed_response = parse_event_info(all_raw_text)
    return parsed_response
