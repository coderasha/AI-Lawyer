from pypdf import PdfReader
import docx
from PIL import Image
import pytesseract
import pandas as pd


def parse_pdf(path):
    reader = PdfReader(path)
    return "\n".join([p.extract_text() or "" for p in reader.pages])


def parse_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])


def parse_csv(path):
    df = pd.read_csv(path)
    return df.to_string()


def parse_image(path):
    try:
        img = Image.open(path)
        return pytesseract.image_to_string(img)
    except Exception:
        return "OCR failed: could not read image"

