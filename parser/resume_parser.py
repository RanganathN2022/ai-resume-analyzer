import pdfplumber
import re

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_experience(text):
    matches = re.findall(r'(\d+)\+?\s*years', text.lower())
    return int(matches[0]) if matches else 0