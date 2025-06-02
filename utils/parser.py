import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import os

def extract_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    text = "\n".join([page.get_text() for page in doc])
    return text

def extract_text_from_image(filepath):
    img = Image.open(filepath)
    return pytesseract.image_to_string(img)
