from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
import tempfile
import os

from app.models.llm import LLM
from app.orchestration.router import ModelRouter
from app.ingestion.parser import parse_image, parse_pdf, parse_docx

router = APIRouter()
router_model = ModelRouter()


def extract_file_text(file_path, filename):
    if filename.endswith(".pdf"):
        return parse_pdf(file_path)
    elif filename.endswith(".docx"):
        return parse_docx(file_path)
    else:
        return parse_image(file_path)


@router.post("/chat")
async def chat(
    message: str = Form(...),
    mode: str = Form("AUTO"),
    model_name: str = Form("llama3"),
    file: UploadFile = File(None)
):

    # Select model
    if mode == "AUTO":
        model_name = router_model.select_model()

    llm = LLM(model_name)

    file_context = ""

    # If user uploaded a file in chat
    if file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        file_context = extract_file_text(tmp_path, file.filename)
        os.remove(tmp_path)

    prompt = f"""
You are a legal assistant.

User question:
{message}

Attached document content:
{file_context}
"""

    def generate():
        for token in llm.stream(prompt):
            yield token

    return StreamingResponse(generate(), media_type="text/plain")
