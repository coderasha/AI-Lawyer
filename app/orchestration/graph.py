import ollama
from app.memory.learning_memory import LearningMemory

memory = LearningMemory()


# ---------------- STREAM LLM ----------------

async def stream_llm(prompt: str):

    stream = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    for chunk in stream:
        if "message" in chunk and "content" in chunk["message"]:
            yield chunk["message"]["content"]


# ---------------- MAIN PIPELINE ----------------

async def run_legal_pipeline(prompt: str):

    # 1. Retrieve learned knowledge
    learned_context = memory.search(prompt)

    if learned_context:
        prompt = f"""
You are a legal AI assistant trained on provided legal documents.

Use the following knowledge while answering:
{learned_context}

User Question:
{prompt}
"""

    # 2. Generate response using llama3 only
    async for token in stream_llm(prompt):
        yield token
