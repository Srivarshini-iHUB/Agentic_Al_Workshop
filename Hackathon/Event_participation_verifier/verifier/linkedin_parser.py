def extract_linkedin_info(text):
    lines = text.split('\n')
    keywords = ["DevFest", "speaker", "AI", "keynote", "event", "Google", "Firebase"]
    extracted = [line for line in lines if any(kw.lower() in line.lower() for kw in keywords)]
    return " ".join(extracted) if extracted else "No relevant event information found."