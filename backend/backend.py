"""
PhishGuard - Flask Backend (Render Deployment Ready)
====================================================
"""

import os
import re
import json
import time
import joblib
from datetime import datetime
from flask import Flask, request, jsonify

# ─────────────────────────────────────────────────────────────
# PATH SETUP
# ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(BASE_DIR, "..")

# ─────────────────────────────────────────────────────────────
# FLASK APP
# ─────────────────────────────────────────────────────────────
app = Flask(
    __name__,
    static_folder=os.path.join(ROOT_DIR, "frontend"),
    static_url_path=""
)

# ─────────────────────────────────────────────────────────────
# MODEL PATHS
# ─────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(
    ROOT_DIR,
    "models",
    "email_detector_model.pkl"
)

VECTORIZER_PATH = os.path.join(
    ROOT_DIR,
    "models",
    "tfidf_vectorizer.pkl"
)

METADATA_PATH = os.path.join(
    ROOT_DIR,
    "models",
    "model_metadata.json"
)

# ─────────────────────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────────────────────
print("[PhishGuard] Loading model artifacts...")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

with open(METADATA_PATH, "r") as f:
    metadata = json.load(f)

print(
    f"[PhishGuard] Model Loaded: "
    f"{metadata['model_name']} | "
    f"Accuracy: {metadata['accuracy']}"
)

# ─────────────────────────────────────────────────────────────
# SESSION STATS
# ─────────────────────────────────────────────────────────────
session_stats = {
    "scanned": 0,
    "ham": 0,
    "spam": 0,
    "phishing": 0,
    "start_time": datetime.now().isoformat()
}

# ─────────────────────────────────────────────────────────────
# SIGNAL WORDS
# ─────────────────────────────────────────────────────────────
SPAM_WORDS = [
    "free", "win", "winner", "prize",
    "urgent", "offer", "discount",
    "buy now", "claim", "refund",
    "promotion", "exclusive"
]

PHISH_WORDS = [
    "verify your account",
    "click the link",
    "update payment",
    "account suspended",
    "security alert",
    "login details",
    "bank account",
    "credit card",
    "reset password"
]

HAM_WORDS = [
    "meeting",
    "project",
    "team",
    "schedule",
    "thank you",
    "regards",
    "attached",
    "conference"
]

# ─────────────────────────────────────────────────────────────
# PREPROCESS FUNCTION
# ─────────────────────────────────────────────────────────────
def preprocess(text):

    if not isinstance(text, str):
        return ""

    text = text.lower()

    text = re.sub(
        r"http\\S+|www\\S+|https\\S+",
        " url ",
        text
    )

    text = re.sub(
        r"\\S+@\\S+",
        " email ",
        text
    )

    text = re.sub(
        r"[^a-z\\s]",
        " ",
        text
    )

    text = re.sub(
        r"\\s+",
        " ",
        text
    ).strip()

    return text

# ─────────────────────────────────────────────────────────────
# SIGNAL WORD DETECTION
# ─────────────────────────────────────────────────────────────
def find_signal_words(text):

    lower = text.lower()

    spam_found = [
        word for word in SPAM_WORDS
        if word in lower
    ]

    phish_found = [
        word for word in PHISH_WORDS
        if word in lower
    ]

    ham_found = [
        word for word in HAM_WORDS
        if word in lower
    ]

    return spam_found, phish_found, ham_found

# ─────────────────────────────────────────────────────────────
# CONFIDENCE
# ─────────────────────────────────────────────────────────────
def get_confidence(label, text):

    spam_n, phish_n, ham_n = find_signal_words(text)

    if label == "phishing":
        confidence = 70 + len(phish_n) * 5

    elif label == "spam":
        confidence = 65 + len(spam_n) * 4

    else:
        confidence = 70 + len(ham_n) * 3

    confidence = max(55, min(98, confidence))

    return int(confidence)

# ─────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────

@app.route("/")
def index():

    return app.send_static_file("index.html")

@app.route("/health")
def health():

    return jsonify({
        "status": "online",
        "model": metadata["model_name"],
        "accuracy": metadata["accuracy"],
        "total_scanned": session_stats["scanned"],
        "uptime_since": session_stats["start_time"]
    })

@app.route("/stats")
def stats():

    return jsonify(session_stats)

@app.route("/predict", methods=["POST"])
def predict():

    start_time = time.time()

    data = request.get_json(silent=True) or {}

    subject = data.get("subject", "")
    body = data.get("body", "")

    if not body.strip():

        return jsonify({
            "error": "Email body is required"
        }), 400

    full_text = f"{subject} {body}"

    clean_text = preprocess(full_text)

    # Vectorize
    features = vectorizer.transform([clean_text])

    # Predict
    prediction = model.predict(features)[0]

    # Signal Words
    spam_words, phish_words, ham_words = find_signal_words(full_text)

    # Confidence
    confidence = get_confidence(prediction, full_text)

    # Update stats
    session_stats["scanned"] += 1
    session_stats[prediction] += 1

    # Messages
    messages = {

        "ham":
        "This email appears legitimate and safe.",

        "spam":
        "This email has been identified as spam. Avoid clicking links.",

        "phishing":
        "WARNING: Possible phishing attempt detected."
    }

    elapsed_ms = round(
        (time.time() - start_time) * 1000,
        2
    )

    return jsonify({

        "label": prediction,

        "confidence": confidence,

        "message": messages[prediction],

        "signal_words": {

            "spam": spam_words[:10],

            "phishing": phish_words[:10],

            "ham": ham_words[:10]
        },

        "stats": session_stats,

        "response_ms": elapsed_ms
    })

# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    print(
        f"[PhishGuard] Running on port {port}"
    )

    app.run(
        host="0.0.0.0",
        port=port
    )