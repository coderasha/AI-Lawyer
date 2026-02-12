from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.models.llm import LLM
from app.orchestration.router import ModelRouter

router = APIRouter()
router_model = ModelRouter()


class ChatRequest(BaseModel):
    message: str
    mode: str = "AUTO"
    model_name: str = "llama3"


@router.post("/chat")
def chat(request: ChatRequest):

    model_name = request.model_name
    if request.mode == "AUTO":
        model_name = router_model.select_model()

    llm = LLM(model_name)

    def generate():
        for token in llm.stream(request.message):
            yield token

    return StreamingResponse(generate(), media_type="text/plain")
