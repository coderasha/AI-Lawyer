from typing import TypedDict
from langgraph.graph import StateGraph

from app.orchestration.router import ModelRouter
from app.models.llm import LLM
from app.memory.learning_memory import LearningMemory
from app.verification.confidence import calculate_confidence, is_confident


class ChatState(TypedDict):
    user_input: str
    mode: str
    model_name: str
    response: str
    confidence: float


router = ModelRouter()
memory = LearningMemory()


def route_model(state: ChatState):
    if state["mode"] == "AUTO":
        state["model_name"] = router.select_model()
    return state


def generate_response(state: ChatState):
    model = LLM(state["model_name"])

    learnings = memory.get_all()
    memory_context = "\n".join([l["content"] for l in learnings])

    prompt = f"""
    Prior Learnings:
    {memory_context}

    User Question:
    {state['user_input']}
    """

    state["response"] = model.generate(prompt)
    return state


def evaluate_confidence(state: ChatState):
    confidence = calculate_confidence(state["response"])
    state["confidence"] = confidence

    if not is_confident(confidence):
        state["response"] = "Insufficient authority found. Human review recommended."

    return state


graph = StateGraph(ChatState)

graph.add_node("route_model", route_model)
graph.add_node("generate_response", generate_response)
graph.add_node("evaluate_confidence", evaluate_confidence)

graph.set_entry_point("route_model")
graph.add_edge("route_model", "generate_response")
graph.add_edge("generate_response", "evaluate_confidence")

legal_graph = graph.compile()
