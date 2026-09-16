# labeling/ml_labeler.py

from db.raws import get_all_articles
from db.ml_labels import save_ml_labels
from labeling.ml_model import load_model


def predict_title(title):
    trained = load_model()

    if trained is None:
        print("No trained model found.")
        return []

    vectorizer, model, labels = trained

    X = vectorizer.transform([title])
    probabilities = model.predict_proba(X)[0]

    results = list(zip(labels, probabilities))
    results.sort(key=lambda x: x[1], reverse=True)

    return results

def label_all_articles(progress_callback=None, log_callback=None):
    trained = load_model()

    if trained is None:
        if log_callback:
            log_callback("No trained model found.")
        return

    vectorizer, model, labels = trained
    articles = get_all_articles()
    total = len(articles)

    if total == 0:
        if log_callback:
            log_callback("No articles found.")
        return

    ml_labels = []
    next_progress = 10

    for i, (raw_id, title) in enumerate(articles, start=1):
        X = vectorizer.transform([title or ""])
        probabilities = model.predict_proba(X)[0]

        for label, score in zip(labels, probabilities):
            if score >= 0.5:
                ml_labels.append(
                    (raw_id, label, float(score))
                )

        progress = int((i / total) * 100)

        if progress >= next_progress:
            if progress_callback:
                progress_callback(progress)

            if log_callback:
                log_callback(f"ML labeling: {i}/{total} articles")

            next_progress += 10

    save_ml_labels(ml_labels)

    if log_callback:
        log_callback(f"ML labeled {total} articles.")

def show_prediction(title):
    print(f"\nTitle: {title}")
    print("Predictions:")

    for label, score in predict_title(title):
        print(f"  {label}: {score:.3f}")