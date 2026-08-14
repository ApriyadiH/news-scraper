# export\report_builder.py
import pandas as pd
from utils import get_cutoff_date 
from db.connection import get_connection

def get_labeled_raw_data(days=None):
    conn = get_connection()
    if days:
        cutoff = get_cutoff_date(days=days).isoformat()
        query = f"""
            SELECT 
                r.id, 
                r.date, 
                r.url, 
                r.source, 
                r.category, 
                r.title, 
                r.content,
                MIN(l.label) as label
            FROM raw r
            LEFT JOIN label l ON r.id = l.raw_id
            WHERE r.date >= '{cutoff}'
            GROUP BY r.id
        """
    else: 
        query = """
            SELECT 
                r.id, 
                r.date, 
                r.url, 
                r.source, 
                r.category, 
                r.title, 
                r.content,
                MIN(l.label) as label
            FROM raw r
            LEFT JOIN label l ON r.id = l.raw_id
            GROUP BY r.id
        """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def build_raw_sheet(df):
    out = df.copy()
    out["News"] = out["label"].apply(lambda x: "News" if x is None or x == "UNLABELED" else "Stock")
    out = out.sort_values(["date", "label"], ascending=[False, True]).reset_index(drop=True)
    out["No"] = range(1, len(out) + 1)

    out = out.rename(columns={
        "date": "Date", 
        "url": "Url", 
        "label": "Label",
        "source": "Source", 
        "category": "Category", 
        "title": "Title"
    })

    return out[["No", "Date", "Url", "News", "Label", "Source", "Category", "Title"]]


def build_cnbc_sheet(df):
    filtered = df[
        (df["source"] == "cnbcindonesia.com") &
        (df["label"].isna() | (df["label"] == "UNLABELED"))
    ].copy()

    filtered["News"] = "News"
    filtered = filtered.sort_values("date", ascending=False).reset_index(drop=True)
    filtered["No"] = range(1, len(filtered) + 1)
    filtered = filtered.rename(columns={
        "date": "Date", 
        "url": "Url", 
        "title": "Title"
    })

    return filtered[["No", "Date", "News", "Url", "Title"]]


def build_stock_sheet(df):
    filtered = df[
        df["label"].notna() & 
        (df["label"] != "UNLABELED")
    ].copy()

    filtered = filtered.sort_values(["date", "label"], ascending=[False, True]).reset_index(drop=True)
    filtered["No"] = range(1, len(filtered) + 1)
    filtered = filtered.rename(columns={
        "date": "Date", 
        "label": "Label", 
        "url": "Url", 
        "title": "Title"
    })

    return filtered[["No", "Date", "Label", "Url", "Title"]]


def build_all_sheets(days=None):
    df = get_labeled_raw_data(days=days)
    return {
        "raw": build_raw_sheet(df),
        "cnbc": build_cnbc_sheet(df),
        "stock": build_stock_sheet(df),
    }