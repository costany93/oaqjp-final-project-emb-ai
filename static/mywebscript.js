const RunSentimentAnalysis = () => {
    const textToAnalyze = document.getElementById("textToAnalyze").value;
    const responseElement = document.getElementById("system_response");
    const query = encodeURIComponent(textToAnalyze);
    const xhttp = new XMLHttpRequest();

    responseElement.textContent = "Analyzing...";
    xhttp.onreadystatechange = function () {
        if (this.readyState !== XMLHttpRequest.DONE) {
            return;
        }

        if (this.status === 200) {
            responseElement.textContent = this.responseText;
        } else {
            responseElement.textContent = this.responseText ||
                "Unable to analyze the text. Please try again.";
        }
    };
    xhttp.open("GET", `emotionDetector?textToAnalyze=${query}`, true);
    xhttp.send();
};
