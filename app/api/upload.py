from fastapi import APIRouter, UploadFile, File
import shutil
import os

from app.ingestion.parser import parse_pdf, parse_docx, parse_csv, parse_image
from app.memory.vector_store import VectorStore

router = APIRouter()
store = VectorStore()

UPLOAD_DIR = "data/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    path = f"{UPLOAD_DIR}/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.endswith(".pdf"):
        text = parse_pdf(path)
    elif file.filename.endswith(".docx"):
        text = parse_docx(path)
    elif file.filename.endswith(".csv"):
        text = parse_csv(path)
    else:
        text = parse_image(path)

    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    store.add_documents(chunks)

    return {"status": "Document learned successfully"}
