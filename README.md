# 🛡️ PhishGuard – Email Spam & Phishing Detection System

**Developer:** Kavin R (23BIT040) — ML Engineer | Atchaya A (23BIT005) — Deployment Engineer  
**Stack:** Python · Scikit-learn · TF-IDF · Linear SVM · Flask · HTML/CSS/JS

---

## 📁 Project Structure

```
phishguard/
├── dataset/
│   ├── emails.csv                  ← 3,700 labelled emails (ham/spam/phishing)
│   └── generate_dataset.py         ← Script to regenerate dataset
│
├── scripts/
│   ├── train_model.py              ← Model training (TF-IDF + SVM)
│   └── test_system.py              ← API & accuracy tests
│
├── models/
│   ├── email_detector_model.pkl    ← Trained SVM model (auto-generated)
│   ├── tfidf_vectorizer.pkl        ← TF-IDF vectorizer (auto-generated)
│   └── model_metadata.json         ← Training metrics
│
├── backend/
│   └── backend.py                  ← Flask REST API
│
├── frontend/
│   └── index.html                  ← Dark cyberpunk UI (standalone too)
│
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the model
```bash
python3 scripts/train_model.py
```
This generates `models/email_detector_model.pkl` and `models/tfidf_vectorizer.pkl`.

### 3. Start the Flask backend
```bash
python3 backend/backend.py
```
Server runs at: **http://localhost:5000**

### 4. Open the frontend
Visit **http://localhost:5000** in your browser.  
*(The frontend also works standalone by opening `frontend/index.html` directly — it falls back to a local rule-based classifier.)*

### 5. Run tests
```bash
python3 scripts/test_system.py
```

---

## 🤖 ML Pipeline

| Stage | Detail |
|-------|--------|
| Dataset | 3,700 emails: 1,500 ham · 1,100 spam · 1,100 phishing |
| Preprocessing | Lowercase, URL/email/phone normalization, regex cleaning |
| Features | TF-IDF (unigrams + bigrams, 25K vocab, sublinear_tf) |
| Models compared | Naive Bayes · Logistic Regression · Linear SVM |
| Selection | Best CV F1-macro via 5-fold StratifiedKFold |
| Class imbalance | `class_weight='balanced'` |
| Serialization | Joblib (model + vectorizer) |

---

## 🌐 API Reference

### `POST /predict`
Classify an email.

**Request:**
```json
{
  "subject": "Your account has been suspended",
  "body": "Dear customer, please verify your credentials immediately..."
}
```

**Response:**
```json
{
  "label": "phishing",
  "confidence": 91,
  "message": "WARNING: This email shows strong phishing characteristics...",
  "signal_words": {
    "phishing": ["verify your credentials", "account has been"],
    "spam": [],
    "ham": []
  },
  "stats": { "scanned": 5, "ham": 2, "spam": 1, "phishing": 2 },
  "response_ms": 12.4
}
```

### `GET /health`
Returns model status and session info.

### `GET /stats`
Returns session-level scan statistics.

---

## 🎨 Frontend Features

- **Category-specific highlighting:**
  - 🟢 Safe email → only green highlights on ham/legitimate words
  - 🔴 Spam detected → only red highlights on spam trigger words
  - 🟠 Phishing → only orange highlights on phishing phrases
- Live session stats (scanned / safe / spam / phishing)
- Confidence bar per prediction
- Detected signal word chips
- Reference panels for spam vs ham words
- Works offline (fallback rule-based classifier)

---

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 100% (test set) |
| CV F1 Macro | 1.00 ± 0.00 |
| Phishing Recall | 1.00 |
| Spam Recall | 1.00 |
| Ham Precision | 1.00 |
| Response Time | < 50ms |

---

## 🔧 Extending the Project

- **Real emails:** Replace `dataset/emails.csv` with a real dataset (Enron, SpamAssassin CSV). Keep columns `text` and `label` (ham/spam/phishing).
- **Add features:** Email headers (From, Reply-To), URL count, HTML tag count.
- **Improve model:** Try XGBoost, Random Forest, or fine-tune a BERT model.
- **Deploy:** Use Gunicorn + Nginx for production.
