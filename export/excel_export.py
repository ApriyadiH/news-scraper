# export\excel_export.py
import os
import pandas as pd
from utils.path_utils import get_desktop_dir

def export_sheets_to_excel(sheets_dict, filename=None, filepath = get_desktop_dir()):

    if filename is None:
        filename = os.path.join(filepath, "report.xlsx")

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with pd.ExcelWriter(filename, engine="openpyxl", mode="w") as writer:
        for sheet_name, df in sheets_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Exported {list(sheets_dict.keys())} to {filename}")

    return filename