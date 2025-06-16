from PyPDF2 import PdfReader

def verify_event_ticket(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    keywords = ["Google", "DevFest", "Ticket", "Pass", "QR", "Session", "2024"]
    found_keywords = [kw for kw in keywords if kw.lower() in text.lower()]

    return len(found_keywords) >= 2, found_keywords