import requests
from bs4 import BeautifulSoup
import os
import hashlib

TARGET_URL = "https://event.zenko-kyo.or.jp/eventList"
STATE_FILE = "state_hash.txt"

def fetch_html():
    r = requests.get(TARGET_URL, timeout=20)
    r.raise_for_status()
    return r.text

def extract_yokohama_counts(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    count = text.count("横浜エリア")
    return count

def compute_hash(count):
    return hashlib.sha256(str(count).encode()).hexdigest()

def load_prev_hash():
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def save_hash(h):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        f.write(h)

def send_line_message(msg):
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.getenv("LINE_USER_ID")

    if not token or not user_id:
        print("LINE token or user ID missing.")
        return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": msg}]
    }
    requests.post(url, headers=headers, json=payload)

def main():
    html = fetch_html()
    count = extract_yokohama_counts(html)
    new_hash = compute_hash(count)

    prev_hash = load_prev_hash()

    if prev_hash != new_hash:
        msg = f"横浜エリアの件数が変化しました: {count}件"
        send_line_message(msg)
        save_hash(new_hash)
        print("Updated and notified.")
    else:
        print("No change detected.")

if __name__ == "__main__":
    main()
