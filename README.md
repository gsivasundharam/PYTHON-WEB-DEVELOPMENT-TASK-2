# 🔍 SentimentIQ — Sentiment Analysis Web App

A Flask web application that analyses text sentiment using TextBlob.
Classifies text as **Positive**, **Negative**, or **Neutral** and displays
polarity + subjectivity scores with a sentence-by-sentence breakdown.

---

## 📁 Project Structure

```
sentiment_app/
├── app.py                  ← Flask backend + TextBlob logic
├── templates/
│   └── index.html          ← Full frontend (dark UI)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download TextBlob corpora (one-time)
python -m textblob.download_corpora

# 3. Run the app
python app.py
```

Open your browser at: **http://localhost:5000**

---

## 🌐 API Endpoint

### `POST /analyse`

**Request body (JSON):**
```json
{ "text": "Your text here..." }
```

**Response (JSON):**
```json
{
  "polarity":           0.45,
  "subjectivity":       0.72,
  "sentiment":          "Positive",
  "sentiment_emoji":    "😊",
  "sentiment_css":      "positive",
  "subjectivity_label": "Highly Subjective",
  "word_count":         42,
  "sentence_count":     3,
  "sentences": [
    {
      "text":         "I loved it!",
      "polarity":     0.5,
      "subjectivity": 0.6,
      "sentiment":    "Positive",
      "css":          "positive"
    }
  ],
  "keywords": ["great product", "fast delivery"]
}
```

---

## 📊 How TextBlob Sentiment Works

| Score | Range | Meaning |
|---|---|---|
| **Polarity** | -1.0 to +1.0 | Negative → Neutral → Positive |
| **Subjectivity** | 0.0 to 1.0 | Objective (fact) → Subjective (opinion) |

**Classification thresholds used:**
- Polarity > 0.1 → **Positive**
- Polarity < -0.1 → **Negative**
- Between → **Neutral**

---

## ✨ Features

- Overall sentiment verdict with emoji
- Polarity & subjectivity score gauges
- Word count and sentence count
- Sentence-by-sentence sentiment breakdown
- Keyword / noun phrase extraction
- 4 built-in sample texts to try
- Ctrl+Enter keyboard shortcut to analyse
