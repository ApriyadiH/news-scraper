# notifications.py
from windows_toasts import Toast, WindowsToaster

def notify_done(message="Scraping and export complete!", title="News Scraper"):
    try:
        toaster = WindowsToaster(title)
        toast = Toast()
        toast.text_fields = [message]
        toaster.show_toast(toast)
    except Exception as e:
        print(f"Notification failed (non-critical): {e}")