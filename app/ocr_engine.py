import os
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import easyocr
from pdfminer.high_level import extract_text as extract_text_from_pdfminer
from utils.log_utils import log_error, log_info

# Initialize OCR Reader once (CPU)
reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image_for_ocr(image_path: str) -> str:
    """
    Preprocesses the image to improve OCR accuracy.
    Converts to grayscale, applies thresholding, and saves a temporary processed file.
    """
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        processed_path = f"{image_path}_processed.png"
        cv2.imwrite(processed_path, img)
        log_info("OCR", f"Preprocessed image saved at {processed_path}")
        return processed_path
    except Exception as e:
        log_error("Preprocess", f"Image preprocessing failed: {e}")
        return image_path  # fallback to original image if preprocessing fails


def extract_text_from_document(file_path: str) -> str:
    """
    Extracts text from both image and PDF documents using EasyOCR, Tesseract, and PDFMiner.
    - For PDFs: tries direct text extraction first (if digital)
    - For scanned PDFs: converts pages to images, then OCR
    - For images: uses preprocessing + OCR
    """
    text_output = ""

    try:
        ext = os.path.splitext(file_path.lower())[1]

        # 🧾 Case 1: PDF File
        if ext == ".pdf":
            log_info("OCR", f"Detected PDF file: {file_path}")

            # Try direct text extraction first (digital PDFs)
            direct_text = extract_text_from_pdfminer(file_path)
            if direct_text and len(direct_text.strip()) > 20:
                log_info("PDFMiner", "Extracted text directly from PDF without OCR.")
                return direct_text

            # If no direct text, fall back to OCR for scanned PDFs
            pages = convert_from_path(file_path)
            if not pages:
                raise ValueError("No pages found in PDF file.")

            for i, page in enumerate(pages):
                page_path = f"{file_path}_page_{i}.png"
                page.save(page_path, "PNG")

                # Run EasyOCR first
                results = reader.readtext(page_path, detail=0)
                page_text = " ".join(results)

                # Backup OCR with Tesseract if EasyOCR fails
                if not page_text.strip():
                    page_text = pytesseract.image_to_string(Image.open(page_path))

                text_output += f"\n{page_text}"
                os.remove(page_path)

        # 🖼️ Case 2: Image File (JPG/PNG)
        else:
            log_info("OCR", f"Detected Image file: {file_path}")

            # Preprocess to improve text clarity
            processed_path = preprocess_image_for_ocr(file_path)

            results = reader.readtext(processed_path, detail=0)
            text_output = " ".join(results)

            # Fallback to Tesseract if EasyOCR fails
            if not text_output.strip():
                text_output = pytesseract.image_to_string(Image.open(processed_path))

            # Remove temporary processed file
            if processed_path != file_path and os.path.exists(processed_path):
                os.remove(processed_path)

    except Exception as e:
        log_error("OCR", f"OCR failed for {file_path}: {e}")
        text_output = ""

    return text_output
