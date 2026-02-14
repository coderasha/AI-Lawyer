from fastapi import APIRouter, UploadFile, File
from app.ingestion.parser import parse_file
from app.memory.learning_memory import LearningMemory
from app.registry.document_registry import DocumentRegistry

router = APIRouter()
memory = LearningMemory()
registry = DocumentRegistry()

@router.post("/upload")
async def upload(file: UploadFile = File(...)):

    content = await file.read()
    text = parse_file(file.filename, content)

    if not text or len(text.strip()) < 50:
        return {"status": "failed", "message": "Document contains no readable text"}

    # store in vector memory
    memory.learn(text)

    # store metadata
    registry.add_document(file.filename, len(text))

    return {
        "status": "success",
        "filename": file.filename,
        "characters_learned": len(text)
    }
