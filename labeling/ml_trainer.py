from db.human_labels import get_training_data
from db.ml_labels import clear_ml_labels
from labeling.ml_model import create_model, save_model
from labeling.ml_labeler import label_all_articles


def train_model(progress_callback=None, log_callback=None):
    rows = get_training_data()

    if not rows:
        if log_callback:
            log_callback("No training data found.")
        return None

    titles = []
    labels = []

    for raw_id, title, human_labels in rows:
        titles.append(title or "")
        labels.append(human_labels.split(","))

    if log_callback:
        log_callback(f"Training on {len(titles)} articles...")

    vectorizer, model = create_model()
    X = vectorizer.fit_transform(titles)

    all_labels = sorted({
        label
        for article_labels in labels
        for label in article_labels
    })

    y = []

    for article_labels in labels:
        y.append([
            1 if label in article_labels else 0
            for label in all_labels
        ])

    model.fit(X, y)
    save_model(vectorizer, model, all_labels)

    if log_callback:
        log_callback("Model trained and saved.")
        log_callback("Clearing old ML labels...")

    clear_ml_labels()

    if log_callback:
        log_callback("Generating new ML labels...")

    label_all_articles(
        progress_callback=progress_callback,
        log_callback=log_callback,
    )

    if log_callback:
        log_callback(f"Trained on {len(titles)} articles.")
        log_callback(f"Labels: {all_labels}")

    return vectorizer, model, all_labels