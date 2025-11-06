import re

def clean_extracted_text(raw_text: str) -> str:
    """Cleans and normalizes OCR text output."""
    if not raw_text:
        return ""
    text = raw_text.lower()
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-z0-9₹.,-/: ]', '', text)
    return text.strip()
