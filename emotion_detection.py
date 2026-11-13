"""Emotion detection client for the Watson NLP service."""

import json

import requests


EMOTION_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
EMOTION_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
    "Content-Type": "application/json",
}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def _empty_result():
    """Return the result shape used when the service rejects empty input."""
    return {emotion: None for emotion in EMOTIONS} | {"dominant_emotion": None}


def emotion_detector(text_to_analyze):
    """Return emotion scores and the dominant emotion for the supplied text."""
    if not isinstance(text_to_analyze, str):
        raise TypeError("text_to_analyze must be a string")
    if not text_to_analyze.strip():
        return _empty_result()

    response = requests.post(
        EMOTION_URL,
        headers=EMOTION_HEADERS,
        json={"raw_document": {"text": text_to_analyze}},
        timeout=30,
    )
    if response.status_code == 400:
        return _empty_result()
    response.raise_for_status()

    response_data = json.loads(response.text)
    emotion_scores = response_data["emotionPredictions"][0]["emotion"]
    result = {emotion: emotion_scores[emotion] for emotion in EMOTIONS}
    result["dominant_emotion"] = max(
        EMOTIONS, key=lambda emotion: result[emotion]
    )
    return result
