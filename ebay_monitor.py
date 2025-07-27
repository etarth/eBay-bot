# ebay_monitor.py

import requests
import time
import json
import os
from config import EBAY_OAUTH_TOKEN, SEARCH_QUERY, CHECK_INTERVAL, RESULT_LIMIT
from email_notifier import send_email_notification

HEADERS = {
    "Authorization": f"Bearer {EBAY_OAUTH_TOKEN}",
    "Content-Type": "application/json"
}

SEEN_FILE = "seen_items.json"

def load_seen_items():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_seen_items(seen_ids):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen_ids), f)

def fetch_new_items(seen_ids):
    url = f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={SEARCH_QUERY}&sort=newlyListed&limit={RESULT_LIMIT}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"[Error] API call failed with status {response.status_code}")
        return []

    items = response.json().get("itemSummaries", [])
    new_items = []

    for item in items:
        item_id = item["itemId"]
        if item_id not in seen_ids:
            seen_ids.add(item_id)
            new_items.append({
                "title": item["title"],
                "price": item["price"]["value"],
                "url": item["itemWebUrl"]
            })

    return new_items

def main():
    print("🚀 eBay Listing Monitor Started!")
    seen_ids = load_seen_items()

    while True:
        try:
            new_items = fetch_new_items(seen_ids)
            if new_items:
                send_email_notification(new_items)
            else:
                print("⏱️ No new items this round.")
        except Exception as e:
            print(f"[Error] {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
