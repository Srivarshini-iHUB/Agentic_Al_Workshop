import pytesseract
import fitz  # PyMuPDF
from PIL import Image
import os

def extract_text_from_pdf(path):
    try:
        doc = fitz.open(path)
        return "\n".join(page.get_text() for page in doc)
    except Exception as e:
        return f"[ERROR extracting PDF: {path}] {e}"

def extract_text_from_image(path):
    try:
        image = Image.open(path)
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"[ERROR extracting image text: {path}] {e}"

def load_student_inputs(folder_path):
    texts = []
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        content = ""

        if file.lower().endswith(".pdf"):
            content = extract_text_from_pdf(file_path)
            tag = "[PDF]"
        elif file.lower().endswith((".png", ".jpg", ".jpeg")):
            content = extract_text_from_image(file_path)
            tag = "[IMAGE]"
        elif file.lower().endswith(".txt"):
            with open(file_path, 'r', encoding="utf-8") as f:
                content = f.read()
            tag = "[TEXT]"
        else:
            continue  # unsupported file type

        # Add file label and content
        texts.append(f"{tag} {file}:\n{content.strip()}\n")

    return "\n\n".join(texts)
