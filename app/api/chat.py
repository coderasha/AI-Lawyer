from fastapi import APIRouter
from pydantic import BaseModel

from app.orchestration.graph import legal_graph
from app.memory.learning_memory import LearningMemory

router = APIRouter()
memory = LearningMemory()


class ChatRequest(BaseModel):
    message: str
    mode: str = "AUTO"
    model_name: str = "llama3"


@router.post("/chat")
def chat(request: ChatRequest):

    if request.message.startswith("/learn"):
        content = request.message.replace("/learn", "").strip()
        memory.add_learning(content)
        return {"status": "Learned successfully."}

    state = {
        "user_input": request.message,
        "mode": request.mode,
        "model_name": request.model_name,
        "response": "",
        "confidence": 0.0
    }

    result = legal_graph.invoke(state)

    return {
        "model_used": result["model_name"],
        "confidence": result["confidence"],
        "response": result["response"]
    }
