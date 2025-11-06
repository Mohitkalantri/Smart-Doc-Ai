# 🧠 Smart Document AI System

Smart Document AI is an **end-to-end intelligent document understanding system** that reads, extracts, and reasons over unstructured business documents such as invoices, resumes, and reports.
Built with **FastAPI**, **EasyOCR**, and **Python**, this project demonstrates real-world AI system design — combining OCR, NLP, and rule-based reasoning into one modular backend.

---

## 🚀 Features

- 📄 **Multi-format Document Support:** Works with both images and PDFs (scanned or digital).
- 🔍 **Accurate Text Extraction:** Uses `EasyOCR`, `Tesseract`, and `pdfminer` for OCR and digital text reading.
- 🧠 **Automated Reasoning:** Validates totals, ranks resumes, and detects missing fields.
- ⚙️ **Clean REST API:** FastAPI-powered endpoint for AI inference.
- 🧩 **Modular Codebase:** Separate layers for OCR, preprocessing, model, and reasoning.
- 💡 **Explainable Results:** Returns structured, human-readable JSON output.
- ⚡ **Error Handling:** Graceful responses for unreadable or invalid documents.

---

## 🧩 Project Structure

```
SmartDocAI/
├── app/
│   ├── api_service.py         # FastAPI app with endpoints
│   ├── ocr_engine.py          # OCR & text extraction (PDF/Image)
│   ├── ai_model_handler.py    # AI field extraction logic
│   ├── decision_engine.py     # Business reasoning layer
│   ├── text_preprocessor.py   # Text cleaning utilities
│   └── explainability_module.py # (Optional) Explainability features
├── utils/
│   ├── file_utils.py          # File type checks and handling
│   └── log_utils.py           # Logging helper
├── data/
│   ├── uploads/               # Temporary storage for uploaded documents
│   └── sample_docs/           # Example PDFs and images for testing
├── models/                    # Placeholder for trained models
├── main.py                    # Entry point for the FastAPI application
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---
## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Mohitkalantri/Smart-Doc-Ai
cd SmartDocAI
```

### 2️⃣ Create and Activate Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

> **💡 Windows Users:**
> Install [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/) for PDF-to-image conversion (needed by `pdf2image`).
> Add the `poppler/bin` folder to your system's PATH.

---

## ▶️ Running the Application

1.  Start the FastAPI server:
    ```bash
    python main.py
    ```
2.  Once it starts, open your browser to:
    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

3.  Use the interactive Swagger UI to upload a document and test the `/api/v1/predict` endpoint.

---

## 🧠 Core Workflow

**Document → OCR Engine → Text Preprocessor → AI Field Extractor → Reasoning Layer → JSON Output**

Each module handles a specific function:

-   **OCR Engine:** Extracts text from scanned or digital documents.
-   **Preprocessor:** Cleans and normalizes text.
-   **AI Model Handler:** Detects document type and extracts key fields.
-   **Reasoning Layer:** Applies business rules and generates decisions.

---

## 🧮 Example API Output

```json
{
  "document_type": "resume",
  "fields_extracted": {
    "document_type": "resume",
    "candidate_name": "Mohit Kalantri",
    "skills": "Python, ML, AI"
  },
  "decision": "Ranked High",
  "confidence_score": 0.9,
  "explainability_map": null
}
```