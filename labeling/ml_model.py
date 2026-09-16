# labeling/ml_model.py

import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier


MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "ml_model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")


def create_model():
    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
    )

    model = OneVsRestClassifier(
        LogisticRegression(max_iter=1000)
    )

    return vectorizer, model


def save_model(vectorizer, model, labels):
    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(
        {
            "model": model,
            "labels": labels,
        },
        MODEL_PATH,
    )

    joblib.dump(vectorizer, VECTORIZER_PATH)

    print("ML model saved.")


def load_model():
    if not os.path.exists(MODEL_PATH):
        return None

    if not os.path.exists(VECTORIZER_PATH):
        return None

    data = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    return vectorizer, data["model"], data["labels"]