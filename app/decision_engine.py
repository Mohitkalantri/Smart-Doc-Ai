def generate_decision(fields: dict) -> dict:
    """Performs rule-based reasoning on extracted fields."""
    try:
        doc_type = fields.get("document_type", "unknown")
        confidence = 0.9

        if doc_type == "invoice":
            amount = fields.get("total_amount", "₹0")
            status = "Valid" if "₹" in amount and amount != "₹0" else "Invalid"
        elif doc_type == "resume":
            status = "Ranked High" if "AI" in fields.get("skills", "") else "Ranked Low"
        else:
            status = "Reviewed"

        return {
            "status": status,
            "confidence": confidence,
            "explainability_map": None
        }

    except Exception as e:
        return {"status": "Error", "confidence": 0.0, "explainability_map": None}
