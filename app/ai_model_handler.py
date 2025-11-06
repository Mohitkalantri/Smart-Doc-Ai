from utils.log_utils import log_info

def extract_document_fields(cleaned_text: str) -> dict:
    """
    Dummy placeholder model logic for field extraction.
    Replace with trained model later (LayoutLMv3, Donut, etc.)
    """
    fields = {}
    try:
        if "invoice" in cleaned_text:
            fields["document_type"] = "invoice"
            fields["vendor"] = "ABC Pvt Ltd" if "abc" in cleaned_text else "Unknown"
            fields["total_amount"] = "₹58,400" if "58,400" in cleaned_text else "₹0"
        elif "resume" in cleaned_text:
            fields["document_type"] = "resume"
            fields["candidate_name"] = "Mohit Kalantri"
            fields["skills"] = "Python, ML, AI"
        else:
            fields["document_type"] = "report"
            fields["summary"] = cleaned_text[:150] + "..."
        log_info("ModelHandler", f"Extracted fields: {fields}")
    except Exception as e:
        log_info("ModelHandler", f"Extraction failed: {e}")
        fields = {}
    return fields
