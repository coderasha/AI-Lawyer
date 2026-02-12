class LLM:

    def __init__(self, name: str):
        self.name = name

    def generate(self, prompt: str) -> str:
        return f"[{self.name}] Response generated for: {prompt[:150]}"
