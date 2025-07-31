import requests
import time
import json
import os
import re
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from config import SEARCH_QUERY, CHECK_INTERVAL, RESULT_LIMIT
from email_notifier import send_email_notification

SEEN_FILE = "seen_items.json"

# Headers to mimic a real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

def load_seen_items():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_seen_items(seen_ids):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen_ids), f)

def extract_item_id_from_url(url):
    """Extract item ID from eBay URL"""
    match = re.search(r'/itm/([^/?]+)', url)
    return match.group(1) if match else None

def clean_price(price_text):
    """Clean and extract price from text"""
    if not price_text:
        return "N/A"
    # Remove extra whitespace and extract price
    price = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
    return price.group() if price else "N/A"

def fetch_new_items(seen_ids):
    # Build eBay search URL
    search_url = f"https://www.ebay.com/sch/i.html?_nkw={quote_plus(SEARCH_QUERY)}&_sop=10&LH_Complete=1&LH_Sold=1&rt=nc"
    
    try:
        response = requests.get(search_url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find item containers (eBay uses different classes, this covers most)
        item_containers = soup.find_all('div', class_=lambda x: x and ('s-item' in x or 'lvresult' in x))
        
        if not item_containers:
            # Try alternative selectors
            item_containers = soup.find_all('li', {'data-view': 'mi:1686|iid'}) or \
                            soup.find_all('div', class_='s-item__wrapper')
        
        new_items = []
        items_processed = 0
        
        for container in item_containers[:RESULT_LIMIT]:
            try:
                # Extract title
                title_elem = container.find('h3') or container.find('a', class_='s-item__link')
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                
                # Extract URL
                link_elem = container.find('a', href=True)
                if not link_elem:
                    continue
                    
                url = link_elem['href']
                item_id = extract_item_id_from_url(url)
                
                if not item_id or item_id in seen_ids:
                    continue
                
                # Extract price
                price_elem = container.find('span', class_=lambda x: x and 'price' in x.lower()) or \
                           container.find('span', string=re.compile(r'\$[\d,]+'))
                
                price = clean_price(price_elem.get_text(strip=True) if price_elem else "N/A")
                
                # Add to seen items and new items list
                seen_ids.add(item_id)
                new_items.append({
                    "title": title,
                    "price": f"${price}",
                    "url": url.split('?')[0]  # Remove tracking parameters
                })
                
                items_processed += 1
                
            except Exception as e:
                print(f"[Item Processing Error] {e}")
                continue
        
        save_seen_items(seen_ids)
        print(f"📊 Processed {items_processed} items, found {len(new_items)} new ones")
        return new_items
        
    except requests.exceptions.RequestException as e:
        print(f"[Network Error] {e}")
        return []
    except Exception as e:
        print(f"[Scraping Error] {e}")
        return []

def main():
    print("🚀 eBay Listing Monitor Started (Web Scraping)!")
    print(f"🔍 Monitoring: '{SEARCH_QUERY}'")
    print(f"⏰ Check interval: {CHECK_INTERVAL} minutes")
    
    seen_ids = load_seen_items()
    print(f"📝 Loaded {len(seen_ids)} previously seen items")

    while True:
        try:
            print(f"\n🔍 Checking for new '{SEARCH_QUERY}' listings...")
            new_items = fetch_new_items(seen_ids)
            
            if new_items:
                print(f"✅ Found {len(new_items)} new items!")
                for item in new_items:
                    print(f"  📦 {item['title'][:50]}... - {item['price']}")
                send_email_notification(new_items)
            else:
                print("⏱️ No new items this round.")
                
        except Exception as e:
            print(f"[Main Loop Error] {e}")

        print(f"💤 Sleeping for {CHECK_INTERVAL} minutes...")
        time.sleep(CHECK_INTERVAL * 60)

if __name__ == "__main__":
    main()