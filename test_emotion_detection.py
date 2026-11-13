"""Unit tests for the emotion detection client."""

import json
import unittest
from unittest.mock import Mock, patch

from emotion_detection import emotion_detector


def make_response(scores, status_code=200):
    """Build a response object matching the Watson service payload."""
    response = Mock()
    response.status_code = status_code
    response.text = json.dumps(
        {"emotionPredictions": [{"emotion": scores}]}
    )
    response.raise_for_status.return_value = None
    return response


class EmotionDetectionTests(unittest.TestCase):
    """Verify dominant-emotion detection for the required examples."""

    def assert_dominant_emotion(self, text, dominant_emotion):
        """Assert the expected dominant emotion for a statement."""
        scores = {
            "anger": 0.01,
            "disgust": 0.02,
            "fear": 0.03,
            "joy": 0.04,
            "sadness": 0.05,
        }
        scores[dominant_emotion] = 0.99
        with patch(
            "emotion_detection.requests.post",
            return_value=make_response(scores),
        ):
            result = emotion_detector(text)
        self.assertEqual(result["dominant_emotion"], dominant_emotion)

    def test_joy(self):
        """Test the joy example."""
        self.assert_dominant_emotion("I am glad this happened", "joy")

    def test_anger(self):
        """Test the anger example."""
        self.assert_dominant_emotion("I am really mad about this", "anger")

    def test_disgust(self):
        """Test the disgust example."""
        self.assert_dominant_emotion(
            "I feel disgusted just hearing about this", "disgust"
        )

    def test_sadness(self):
        """Test the sadness example."""
        self.assert_dominant_emotion("I am so sad about this", "sadness")

    def test_fear(self):
        """Test the fear example."""
        self.assert_dominant_emotion(
            "I am really afraid that this will happen", "fear"
        )

    @patch(
        "emotion_detection.requests.post",
        return_value=make_response({}, status_code=400),
    )
    def test_blank_input_returns_empty_result(self, _post):
        """Test the required response for blank input."""
        result = emotion_detector("")
        self.assertEqual(result, {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        })


if __name__ == "__main__":
    unittest.main()
