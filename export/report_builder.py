# export\report_builder.py

import pandas as pd
from utils.date_utils import get_cutoff_date
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
    out["News"] = out["label"].apply(
        lambda x: "News" if x is None or x == "UNLABELED" else "Stock"
    )
    out = out.sort_values(["date", "label"], ascending=[False, True]).reset_index(
        drop=True
    )
    out["No"] = range(1, len(out) + 1)

    out = out.rename(
        columns={
            "date": "Date",
            "url": "Url",
            "label": "Label",
            "source": "Source",
            "category": "Category",
            "title": "Title",
        }
    )

    return out[["No", "Date", "Url", "News", "Label", "Source", "Category", "Title"]]


def build_cnbc_sheet(df):
    filtered = df[
        (df["source"] == "cnbcindonesia.com")
        & (df["label"].isna() | (df["label"] == "UNLABELED"))
    ].copy()

    filtered["News"] = "News"
    filtered = filtered.sort_values("date", ascending=False).reset_index(drop=True)
    filtered["No"] = range(1, len(filtered) + 1)
    filtered = filtered.rename(columns={"date": "Date", "url": "Url", "title": "Title"})

    return filtered[["No", "Date", "News", "Url", "Title"]]


def build_stock_sheet(df):
    filtered = df[df["label"].notna() & (df["label"] != "UNLABELED")].copy()

    filtered = filtered.sort_values(
        ["date", "label"], ascending=[False, True]
    ).reset_index(drop=True)
    filtered["No"] = range(1, len(filtered) + 1)
    filtered = filtered.rename(
        columns={"date": "Date", "label": "Label", "url": "Url", "title": "Title"}
    )

    return filtered[["No", "Date", "Label", "Url", "Title"]]


def build_all_sheets(days=None):
    df = get_labeled_raw_data(days=days)
    return {
        "raw": build_raw_sheet(df),
        "cnbc": build_cnbc_sheet(df),
        "stock": build_stock_sheet(df),
    }


def get_labeled_raw_data_by_date(start_date=None, end_date=None, all_date=False):
    conn = get_connection()

    if all_date:
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
            WHERE r.date >= ?
              AND r.date <= ?
            GROUP BY r.id
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=[
                start_date.isoformat(),
                end_date.isoformat(),
            ],
        )

    conn.close()
    return df

def build_kopas_sheets(df):
    filtered = df[df["label"].notna() & (df["label"] != "UNLABELED")].copy()

    filtered["date"] = pd.to_datetime(filtered["date"])

    filtered = filtered.sort_values(
        ["date", "label"],
        ascending=[False, True],
    )

    kopas_sheets = {}

    for month, month_df in filtered.groupby(filtered["date"].dt.month):
        sheet_name = f"kopas {month}"

        out = month_df.copy()

        out["Date"] = out["date"]
        out["Code"] = out["label"]
        out["News"] = out["title"]
        out["Link"] = "OPEN"
        out["URL"] = out["url"]

        kopas_sheets[sheet_name] = out[
            ["Date", "Code", "News", "Link", "URL"]
        ].reset_index(drop=True)

    return kopas_sheets

def build_all_sheets_by_date(
    start_date=None,
    end_date=None,
    all_date=False,
):
    df = get_labeled_raw_data_by_date(
        start_date=start_date,
        end_date=end_date,
        all_date=all_date,
    )

    sheets = {
        "raw": build_raw_sheet(df),
        "cnbc": build_cnbc_sheet(df),
        "stock": build_stock_sheet(df),
    }

    sheets.update(build_kopas_sheets(df))

    return sheets
