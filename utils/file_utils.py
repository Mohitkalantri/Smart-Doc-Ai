import os

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}

def validate_uploaded_file(filename: str) -> bool:
    """Validate file extension before processing."""
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS
