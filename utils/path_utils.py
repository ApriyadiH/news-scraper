# utils\path_utils.py
import sys
import os
import ctypes
from ctypes import wintypes

def get_app_data_dir():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.join(os.environ["LOCALAPPDATA"], "NewsScraperApp")
    else:
        base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

    os.makedirs(base_dir, exist_ok=True)
    return base_dir

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_desktop_dir():
    CSIDL_DESKTOPDIRECTORY = 0x0010

    path = ctypes.create_unicode_buffer(wintypes.MAX_PATH)

    result = ctypes.windll.shell32.SHGetFolderPathW(
        None,
        CSIDL_DESKTOPDIRECTORY,
        None,
        0,
        path
    )

    if result != 0:
        raise OSError("Could not determine Desktop path")

    return path.value