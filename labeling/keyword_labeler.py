# labeling\keyword_labeler.py
import re
from db.articles import get_unlabeled_articles, mark_as_labeled
from db.keywords import get_all_keywords
from db.labels import insert_label

UNLABELED_TAG = "UNLABELED"

def match_labels(title, keyword_rows):
    matched = []

    for keyword, label in keyword_rows:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, title) and label not in matched:
            matched.append(label)

    return matched

def run_labeling(limit=None):
    keyword_rows = sorted(get_all_keywords(), key=lambda x: x[1])
    unlabeled = get_unlabeled_articles(limit=limit)
    total = len(unlabeled)

    if total == 0:
        print("No unlabeled articles found.")
        return
    
    print(f"Found {total} unlabeled articles. Starting labeling...")
    next_checkpoint = 10

    for i, (raw_id, title) in enumerate(unlabeled, start=1):
        labels = match_labels(title, keyword_rows)

        if labels:
            for label in labels:
                insert_label(raw_id, label)
        else:
            insert_label(raw_id, UNLABELED_TAG)

        mark_as_labeled(raw_id)

        progress_percent = (i / total) * 100
        if progress_percent >= next_checkpoint:
            print(f"  {int(progress_percent)}% ({i}/{total}) labeled...")
            next_checkpoint += 10

    print(f"Labeling complete: processed {total} articles.")