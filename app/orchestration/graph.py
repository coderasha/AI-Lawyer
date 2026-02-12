from typing import TypedDict, List
from langgraph.graph import StateGraph

from app.orchestration.router import ModelRouter
from app.models.llm import LLM
from app.memory.learning_memory import LearningMemory
from app.memory.vector_store import VectorStore
from app.verification.confidence import calculate_confidence, is_confident


# ---------------- STATE ---------------- #

class ChatState(TypedDict):
    user_input: str
    mode: str
    model_name: str
    retrieved_docs: List[str]
    learned_memory: List[str]
    response: str
    confidence: float


# Initialize shared components
router = ModelRouter()
learning_memory = LearningMemory()
vector_store = VectorStore()


# ---------------- NODES ---------------- #

def route_model(state: ChatState):
    """Select model automatically if AUTO mode"""
    if state["mode"] == "AUTO":
        state["model_name"] = router.select_model()
    return state


def retrieve_knowledge(state: ChatState):
    """Fetch relevant documents from vector database"""
    docs = vector_store.search(state["user_input"])
    state["retrieved_docs"] = docs if docs else []
    return state


def load_learnings(state: ChatState):
    """Load persistent /learn memory"""
    memories = learning_memory.get_all()
    state["learned_memory"] = [m["content"] for m in memories] if memories else []
    return state


def generate_response(state: ChatState):
    """Create final prompt and call LLM"""

    model = LLM(state["model_name"])

    context_docs = "\n\n".join(state["retrieved_docs"])
    learned_context = "\n\n".join(state["learned_memory"])

    prompt = f"""
You are a careful senior legal advisor.

Follow these rules:
- Prefer provided knowledge over assumptions
- If facts missing, ask questions
- If unsure, say you are unsure
- Do not invent laws

---------------- LEARNED KNOWLEDGE ----------------
{learned_context}

---------------- DOCUMENT KNOWLEDGE ----------------
{context_docs}

---------------- USER QUESTION ----------------
{state['user_input']}
"""

    state["response"] = model.generate(prompt)
    return state


def evaluate_confidence(state: ChatState):
    """Apply safety confidence filter"""
    confidence = calculate_confidence(state["response"])
    state["confidence"] = confidence

    if not is_confident(confidence):
        state["response"] = (
            "I do not have sufficient reliable authority to answer confidently. "
            "Please provide more documents or clarify the situation."
        )

    return state


# ---------------- GRAPH ---------------- #

graph = StateGraph(ChatState)

graph.add_node("route_model", route_model)
graph.add_node("retrieve_knowledge", retrieve_knowledge)
graph.add_node("load_learnings", load_learnings)
graph.add_node("generate_response", generate_response)
graph.add_node("evaluate_confidence", evaluate_confidence)

graph.set_entry_point("route_model")

graph.add_edge("route_model", "retrieve_knowledge")
graph.add_edge("retrieve_knowledge", "load_learnings")
graph.add_edge("load_learnings", "generate_response")
graph.add_edge("generate_response", "evaluate_confidence")

legal_graph = graph.compile()
