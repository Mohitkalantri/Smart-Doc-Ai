from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os, uuid, shutil

from app.ocr_engine import extract_text_from_document
from app.text_preprocessor import clean_extracted_text
from app.ai_model_handler import extract_document_fields
from app.decision_engine import generate_decision
from utils.file_utils import validate_uploaded_file
from utils.log_utils import log_error, log_info

app = FastAPI(
    title="Smart Document AI 🧠",
    version="1.0",
    description="AI System for Document Understanding & Decision Making"
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "Welcome to Smart Document AI! Upload files at /api/v1/predict"}

@app.post("/api/v1/predict")
async def predict_document(file: UploadFile = File(...)):
    """Handles file upload, extraction, reasoning, and JSON response generation."""

    # Step 1: Validate uploaded file
    if not validate_uploaded_file(file.filename):
        raise HTTPException(status_code=400, detail="Unsupported file type. Use .jpg, .jpeg, .png, or .pdf only.")

    # Step 2: Save file securely
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        log_info("FileSaved", f"File saved successfully as {file_path}")
    except Exception as e:
        log_error("FileSaveError", e)
        raise HTTPException(status_code=500, detail="Failed to save the uploaded file.")

    # Step 3: Pipeline Execution
    try:
        # OCR
        extracted_text = extract_text_from_document(file_path)
        if not extracted_text.strip():
            raise ValueError("No readable text found in the document.")

        # Preprocess
        cleaned_text = clean_extracted_text(extracted_text)

        # AI Field Extraction
        extracted_fields = extract_document_fields(cleaned_text)
        if not extracted_fields:
            raise ValueError("No key fields detected from the document.")

        # Reasoning / Decision
        decision_result = generate_decision(extracted_fields)

        response = {
            "document_type": extracted_fields.get("document_type", "unknown"),
            "fields_extracted": extracted_fields,
            "decision": decision_result.get("status", "Unknown"),
            "confidence_score": decision_result.get("confidence", 0.0),
            "explainability_map": decision_result.get("explainability_map", None)
        }

        log_info("Success", f"Document processed successfully: {file.filename}")
        return JSONResponse(content=response)

    except ValueError as ve:
        log_error("ValidationError", ve)
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        log_error("ProcessingError", e)
        raise HTTPException(status_code=500, detail="Internal processing error.")
