"""
PhishGuard - Model Training Script
===================================
Trains a Linear SVM classifier on TF-IDF features to classify emails as:
  - ham       (legitimate)
  - spam      (unsolicited bulk email)
  - phishing  (credential theft / social engineering)

Run:  python3 scripts/train_model.py
"""

import os
import sys
import json
import re
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score, roc_auc_score
)
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────
DATASET_PATH  = os.path.join(os.path.dirname(__file__), "../dataset/emails.csv")
MODELS_DIR    = os.path.join(os.path.dirname(__file__), "../models")
MODEL_PATH    = os.path.join(MODELS_DIR, "email_detector_model.pkl")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")
METADATA_PATH = os.path.join(MODELS_DIR, "model_metadata.json")

os.makedirs(MODELS_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────
# TEXT PREPROCESSING
# ─────────────────────────────────────────────────────────────
def preprocess(text):
    """Clean and normalize email text."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', ' url ', text, flags=re.MULTILINE)
    # Remove email addresses
    text = re.sub(r'\S+@\S+', ' email ', text)
    # Remove phone numbers
    text = re.sub(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', ' phone ', text)
    # Normalize currency amounts
    text = re.sub(r'\$[\d,]+', ' money ', text)
    text = re.sub(r'#\d+', ' id ', text)
    # Keep letters, spaces, common punctuation
    text = re.sub(r'[^a-z\s]', ' ', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ─────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────
print("=" * 60)
print("  PHISHGUARD - MODEL TRAINING")
print("=" * 60)

print(f"\n[1/6] Loading dataset from: {DATASET_PATH}")
df = pd.read_csv(DATASET_PATH)
print(f"      Total emails: {len(df)}")
print(f"      Label distribution:\n{df['label'].value_counts().to_string()}")

# Preprocess text
print("\n[2/6] Preprocessing email text...")
df['clean_text'] = df['text'].apply(preprocess)

# Drop empty rows
df = df[df['clean_text'].str.strip() != '']
print(f"      Rows after cleaning: {len(df)}")

X = df['clean_text'].values
y = df['label'].values

# ─────────────────────────────────────────────────────────────
# TRAIN / TEST SPLIT
# ─────────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\n[3/6] Train/Test split: {len(X_train)} train / {len(X_test)} test")

# ─────────────────────────────────────────────────────────────
# TF-IDF VECTORIZATION
# ─────────────────────────────────────────────────────────────
print("\n[4/6] Building TF-IDF features (unigrams + bigrams)...")
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    max_features=25000,
    sublinear_tf=True,
    min_df=2,
    strip_accents='unicode',
    analyzer='word',
    token_pattern=r'\b[a-z]{2,}\b'
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf  = vectorizer.transform(X_test)
print(f"      Vocabulary size: {len(vectorizer.vocabulary_)}")
print(f"      Feature matrix: {X_train_tfidf.shape}")

# ─────────────────────────────────────────────────────────────
# MODEL COMPARISON
# ─────────────────────────────────────────────────────────────
print("\n[5/6] Training and comparing models...")

models = {
    "Naive Bayes":         MultinomialNB(alpha=0.1),
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42, C=1.0),
    "Linear SVM":          LinearSVC(class_weight='balanced', random_state=42, C=1.0, max_iter=2000),
}

results = {}
for name, model in models.items():
    # Cross-validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X_train_tfidf, y_train, cv=cv, scoring='f1_macro', n_jobs=-1)
    model.fit(X_train_tfidf, y_train)
    y_pred = model.predict(X_test_tfidf)
    acc = accuracy_score(y_test, y_pred)
    results[name] = {
        "model": model,
        "accuracy": acc,
        "cv_mean": cv_scores.mean(),
        "cv_std": cv_scores.std(),
        "y_pred": y_pred
    }
    print(f"\n  ── {name}")
    print(f"     Test Accuracy:      {acc:.4f}")
    print(f"     CV F1 (macro):      {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# ─────────────────────────────────────────────────────────────
# SELECT BEST MODEL
# ─────────────────────────────────────────────────────────────
best_name = "Linear SVM"  # Finalized: best for high-dimensional sparse TF-IDF spaces
best = results[best_name]
best_model = best['model']
y_pred = best['y_pred']

print(f"\n  ✅ Best model: {best_name} (CV F1 = {best['cv_mean']:.4f})")

# ─────────────────────────────────────────────────────────────
# DETAILED EVALUATION
# ─────────────────────────────────────────────────────────────
print("\n[6/6] Detailed Evaluation of Best Model")
print("-" * 60)
print(classification_report(y_test, y_pred, target_names=sorted(set(y))))

cm = confusion_matrix(y_test, y_pred, labels=sorted(set(y)))
labels = sorted(set(y))
print("Confusion Matrix:")
print(f"{'':>12}", end="")
for l in labels:
    print(f"  {l[:8]:>8}", end="")
print()
for i, row in enumerate(cm):
    print(f"  {labels[i][:10]:>10}", end="")
    for val in row:
        print(f"  {val:>8}", end="")
    print()

# ─────────────────────────────────────────────────────────────
# SAVE ARTIFACTS
# ─────────────────────────────────────────────────────────────
joblib.dump(best_model, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)
print(f"\n  Model saved:      {MODEL_PATH}")
print(f"  Vectorizer saved: {VECTORIZER_PATH}")

# Save metadata
metadata = {
    "model_name": best_name,
    "accuracy": round(best['accuracy'], 4),
    "cv_f1_mean": round(best['cv_mean'], 4),
    "cv_f1_std": round(best['cv_std'], 4),
    "classes": labels,
    "vocab_size": len(vectorizer.vocabulary_),
    "train_samples": len(X_train),
    "test_samples": len(X_test),
}
with open(METADATA_PATH, 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"  Metadata saved:   {METADATA_PATH}")

print("\n" + "=" * 60)
print("  TRAINING COMPLETE")
print("=" * 60)
