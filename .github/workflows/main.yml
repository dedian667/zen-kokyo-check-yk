import requests
from bs4 import BeautifulSoup
import os
import re

TARGET_URL = "https://event.zenko-kyo.or.jp/eventList"
STATE_FILE = "yokohama_dates.txt"


def fetch_html():
    r = requests.get(TARGET_URL, timeout=20)
    r.raise_for_status()
    return r.text


def extract_yokohama_dates(html):
    """
    横浜エリア｜ 11月15日開催
    のような形式の日付だけを抽出する
    """
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    # 正規表現で「横浜エリア｜ ◯月◯日開催」を抽出
    pattern = r"横浜エリア[^\d]*(\d{1,2}月\d{1,2}日)開催"
    dates = re.findall(pattern, text)

    return sorted(set(dates))  # 重複削除＆ソート


def load_previous_dates():
    if not os.path.exists(STATE_FILE):
        return []
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def save_dates(dates):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        for d in dates:
            f.write(d + "\n")


def send_line_message(msg):
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    user = os.getenv("LINE_USER_ID")

    if not token or not user:
        print("❌ LINE token or userId が設定されていません")
        return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "to": user,
        "messages": [{"type": "text", "text": msg}]
    }

    r = requests.post(url, headers=headers, json=payload)
    print("LINE Response:", r.status_code, r.text)


def main():
    html = fetch_html()
    new_dates = extract_yokohama_dates(html)
    old_dates = load_previous_dates()

    print("検出された日付:", new_dates)
    print("保存されていた日付:", old_dates)

    # 差分を抽出
    added = [d for d in new_dates if d not in old_dates]

    if added:
        msg = "【新規 横浜エリアイベント】\n" + "\n".join(added)
        send_line_message(msg)
        print("新規イベント通知:", added)
    else:
        print("新規イベントなし")

    # 状態保存
    save_dates(new_dates)


if __name__ == "__main__":
    main()
