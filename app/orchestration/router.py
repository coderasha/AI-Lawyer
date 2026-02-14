class ModelRouter:

    def select_model(self, prompt: str) -> str:
        """
        Decide which LLM should answer the query
        based on the nature of the task
        """

        prompt_lower = prompt.lower()

        # ---- Legal reasoning / long answers ----
        legal_keywords = [
            "legal", "law", "section", "contract", "agreement",
            "liable", "liability", "notice", "court", "sue",
            "breach", "damages", "penalty", "act", "ipc"
        ]

        # ---- Document analysis ----
        doc_keywords = [
            "analyze", "review", "summarize", "explain document",
            "what does this notice mean"
        ]

        # ---- Quick factual queries ----
        simple_keywords = [
            "define", "meaning", "what is", "who is"
        ]

        if any(k in prompt_lower for k in legal_keywords):
            return "llama3"   # best reasoning

        if any(k in prompt_lower for k in doc_keywords):
            return "llama3"   # document understanding

        if any(k in prompt_lower for k in simple_keywords):
            return "mistral"  # faster cheaper model

        # default
        return "llama3"
