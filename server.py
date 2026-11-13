"""Flask web server for the emotion detection application."""

from flask import Flask, render_template, request
from requests.exceptions import RequestException

from emotion_detection import emotion_detector


app = Flask(__name__)


@app.route("/")
def home():
    """Render the emotion detection form."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Analyze the submitted text and return a human-readable response."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    try:
        result = emotion_detector(text_to_analyze)
    except RequestException:
        return (
            "The emotion detection service is unavailable. "
            "Please try again from the Skills Network environment."
        ), 502
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    scores = ", ".join(
        f"'{emotion}': {result[emotion]}" for emotion in (
            "anger", "disgust", "fear", "joy", "sadness"
        )
    )
    return (
        f"For the given statement, the system response is {scores}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
