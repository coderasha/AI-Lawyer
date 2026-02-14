from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from app.orchestration.graph import run_legal_pipeline
from app.ingestion.parser import parse_file
import asyncio

router = APIRouter()


@router.post("/chat")
async def chat(
    message: str = Form(...),
    file: UploadFile | None = File(None),
):

    context_text = ""

    # -------- Read attached document --------
    if file is not None:
        content = await file.read()
        context_text = parse_file(file.filename, content)

    final_prompt = message

    if context_text:
        final_prompt = f"""
User Question:
{message}

Attached Document:
{context_text}

Answer using this document if relevant.
"""

    # -------- Stream response --------
    async def stream():
        async for token in run_legal_pipeline(final_prompt):
            yield token
            await asyncio.sleep(0.01)

    return StreamingResponse(stream(), media_type="text/plain")
