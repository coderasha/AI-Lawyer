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

    # learn knowledge
    memory.learn(text)

    # record metadata
    registry.add_document(file.filename, len(text))

    return {
        "status": "success",
        "file": file.filename,
        "characters": len(text)
    }
