"""
Sentiment Analysis Web App
Flask + TextBlob backend — with auto corpus download
"""

from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# ── Auto-download required NLTK/TextBlob corpora on startup ──────────────────
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

for corpus in ['punkt', 'punkt_tab', 'averaged_perceptron_tagger',
               'averaged_perceptron_tagger_eng', 'brown', 'wordnet',
               'stopwords', 'omw-1.4']:
    try:
        nltk.download(corpus, quiet=True)
    except Exception:
        pass

# ── Helpers ───────────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text.strip())


def classify_sentiment(polarity: float) -> dict:
    if polarity > 0.1:
        return {"label": "Positive", "emoji": "😊", "css": "positive"}
    elif polarity < -0.1:
        return {"label": "Negative", "emoji": "😞", "css": "negative"}
    else:
        return {"label": "Neutral", "emoji": "😐", "css": "neutral"}


def classify_subjectivity(score: float) -> str:
    if score < 0.3:
        return "Very Objective"
    elif score < 0.5:
        return "Mostly Objective"
    elif score < 0.7:
        return "Mostly Subjective"
    else:
        return "Highly Subjective"


def analyse(text: str) -> dict:
    from textblob import TextBlob
    blob         = TextBlob(clean_text(text))
    polarity     = round(blob.sentiment.polarity,     4)
    subjectivity = round(blob.sentiment.subjectivity, 4)
    sentiment    = classify_sentiment(polarity)
    word_count   = len(blob.words)

    # Per-sentence breakdown
    sentences = []
    for sent in blob.sentences:
        sp = round(sent.sentiment.polarity,     3)
        ss = round(sent.sentiment.subjectivity, 3)
        sentences.append({
            "text":         str(sent),
            "polarity":     sp,
            "subjectivity": ss,
            "sentiment":    classify_sentiment(sp)["label"],
            "css":          classify_sentiment(sp)["css"],
        })

    # Keywords — noun phrases, safe fallback
    try:
        keywords = list({
            phrase.lower()
            for phrase in blob.noun_phrases
            if len(phrase) > 2
        })[:10]
    except Exception:
        keywords = []

    return {
        "polarity":           polarity,
        "subjectivity":       subjectivity,
        "sentiment":          sentiment["label"],
        "sentiment_emoji":    sentiment["emoji"],
        "sentiment_css":      sentiment["css"],
        "subjectivity_label": classify_subjectivity(subjectivity),
        "word_count":         word_count,
        "sentence_count":     len(blob.sentences),
        "sentences":          sentences,
        "keywords":           keywords,
    }


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyse", methods=["POST"])
def analyse_route():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided."}), 400
    if len(text) > 5000:
        return jsonify({"error": "Text too long. Max 5000 characters."}), 400

    try:
        result = analyse(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=5000)
