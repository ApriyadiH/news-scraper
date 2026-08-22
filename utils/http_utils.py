# utils\http_utils.py
import time
import requests

def fetch_page(url, headers=None, retries=3, timeout=15):
    for attempt in range(retries):
        try:
            resp = requests.get(
                url,
                headers=headers,
                timeout=timeout
            )

            if resp.status_code == 200:
                return resp

            if resp.status_code == 403:
                print(f"403 Forbidden: {url}")
                return None

            if resp.status_code == 404:
                print(f"404 Not Found: {url}")
                return None

            if resp.status_code == 429:
                print(f"429 Too Many Requests: {url}")
                time.sleep(5)
                continue

            if 500 <= resp.status_code < 600:
                print(
                    f"Server error {resp.status_code}: "
                    f"{url} (attempt {attempt + 1}/{retries})"
                )
                time.sleep(3)
                continue

            print(f"HTTP {resp.status_code}: {url}")
            return None

        except requests.RequestException as e:
            print(
                f"Request failed: {url} "
                f"(attempt {attempt + 1}/{retries}): {e}"
            )
            time.sleep(3)

    return None