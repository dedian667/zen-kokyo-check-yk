# Yokohama Event Monitor

This project monitors the number of "横浜エリア" occurrences on:
https://event.zenko-kyo.or.jp/eventList

If the number changes, a LINE Bot message is sent.

## Setup
1. Upload to GitHub
2. Add GitHub Secrets:
   - LINE_CHANNEL_ACCESS_TOKEN
   - LINE_USER_ID
3. Actions run every 5 minutes.
