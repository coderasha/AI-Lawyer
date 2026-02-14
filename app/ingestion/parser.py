import io
import csv
from docx import Document
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image


def parse_file(filename: str, content: bytes) -> str:

    filename = filename.lower()

    try:

        # ---------------- PDF ----------------
        if filename.endswith(".pdf"):
            reader = PdfReader(io.BytesIO(content))
            text = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            return text.strip()

        # ---------------- DOCX ----------------
        elif filename.endswith(".docx"):
            doc = Document(io.BytesIO(content))
            text = "\n".join([p.text for p in doc.paragraphs])
            return text.strip()

        # ---------------- CSV ----------------
        elif filename.endswith(".csv"):
            decoded = content.decode("utf-8", errors="ignore")
            reader = csv.reader(decoded.splitlines())
            text = "\n".join([", ".join(row) for row in reader])
            return text.strip()

        # ---------------- IMAGE (OCR) ----------------
        elif filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
            image = Image.open(io.BytesIO(content))
            text = pytesseract.image_to_string(image)
            return text.strip()

        # ---------------- TXT ----------------
        elif filename.endswith(".txt"):
            return content.decode("utf-8", errors="ignore").strip()

        else:
            return ""

    except Exception as e:
        print("Parsing failed:", e)
        return ""
