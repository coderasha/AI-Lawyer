from app.models.registry import MODEL_REGISTRY


class ModelRouter:

    def score_model(self, model_data):
        return (
            model_data["accuracy"] * 0.5 +
            model_data["speed"] * 0.2 -
            model_data["hallucination_risk"] * 0.3
        )

    def select_model(self):
        best_model = None
        best_score = -1

        for name, data in MODEL_REGISTRY.items():
            score = self.score_model(data)
            if score > best_score:
                best_score = score
                best_model = name

        return best_model
