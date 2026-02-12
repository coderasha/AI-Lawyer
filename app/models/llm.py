import ollama


class LLM:

    def __init__(self, name: str):
        self.name = name

    def generate(self, prompt: str) -> str:
        try:
            response = ollama.chat(
                model=self.name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a senior legal advisor. "
                            "Give structured, cautious legal guidance. "
                            "Ask clarifying questions if facts are missing. "
                            "Do not hallucinate laws."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response["message"]["content"]

        except Exception as e:
            return f"Model error: {str(e)}"
