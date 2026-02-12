import ollama


class LLM:

    def __init__(self, name: str):
        self.name = name

    def stream(self, prompt: str):
        response = ollama.chat(
            model=self.name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a senior legal advisor. "
                        "Give structured, cautious legal guidance. "
                        "Ask clarifying questions if facts are missing."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            stream=True
        )

        for chunk in response:
            if "message" in chunk:
                yield chunk["message"]["content"]
