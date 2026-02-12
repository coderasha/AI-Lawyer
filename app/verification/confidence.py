from app.config.settings import settings


def calculate_confidence(response: str) -> float:
    if len(response) > 20:
        return 0.7
    return 0.4


def is_confident(confidence: float) -> bool:
    return confidence >= settings.CONFIDENCE_THRESHOLD
