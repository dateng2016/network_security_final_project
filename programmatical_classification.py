from selenium import webdriver
from typing import List
import pandas as pd
from selenium.webdriver.chrome.options import Options
import json
import argparse
from math import ceil
import threading

# Number of website chunks to split into
NUM_CHUNKS = 10

# Thread-safe lock for shared data access
lock = threading.Lock()

parser = argparse.ArgumentParser(
    description="Scrape cookies in desktop or mobile mode."
)
parser.add_argument(
    "--mobile", action="store_true", help="Run browser in mobile emulation mode"
)
args = parser.parse_args()

NUM_WEBSITES = 1000
IS_MOBILE = args.mobile

print(f'is mobile ? -> {IS_MOBILE}')

COOKIES_JSON_FILE_NAME = (
    "mobile_cookies.json" if IS_MOBILE else "website_cookies.json"
)

# Read the cookie classification database
df = pd.read_csv("open-cookie-database.csv")
name_to_category = dict()
to_delete_arr = set()

for idx, row in df.iterrows():
    name = row["Cookie / Data Key name"]
    category = row["Category"]
    if name in name_to_category and category != name_to_category[name]:
        to_delete_arr.add(name)
    name_to_category[name] = category

# Remove conflicting cookie names
for to_delete in to_delete_arr:
    name_to_category.pop(to_delete)

# Shared dict for all collected cookies
website_to_cookies = dict()

def get_cookies(url_arr: List[str]):
    options = Options()
    options.add_argument("--headless")
    if IS_MOBILE:
        options.add_argument(
            "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        )

    driver = webdriver.Chrome(options=options)

    try:
        for url in url_arr:
            full_url = "https://www." + url
            try:
                driver.get(full_url)
                cookies = driver.get_cookies()
                with lock:
                    website_to_cookies[url] = cookies
                print(f"[+] Fetched cookies for: {url}")
            except Exception as e:
                print(f"[!] Error on {url}: {e}")
    finally:
        driver.quit()

# Read and clean the top websites list
with open("top-10000-domains", "r") as file:
    website_arr = [w.strip() for w in file.readlines()][:NUM_WEBSITES]

# Split websites into chunks
chunk_size = ceil(len(website_arr) / NUM_CHUNKS)
website_chunks_arr = [
    website_arr[i:i + chunk_size] for i in range(0, len(website_arr), chunk_size)
]

# Start threads for each chunk
threads_arr = []
for website_chunk in website_chunks_arr:
    t = threading.Thread(target=get_cookies, args=(website_chunk,))
    t.start()
    threads_arr.append(t)

# Wait for all threads to finish
for t in threads_arr:
    t.join()

# Classify cookies
for website, cookies_arr in website_to_cookies.items():
    if not cookies_arr:
        continue
    for cookie in cookies_arr:
        name = cookie.get("name")
        cookie["classification"] = name_to_category.get(name)

# Save to JSON
with open(COOKIES_JSON_FILE_NAME, "w") as file:
    json.dump(website_to_cookies, file, indent=4)

print(f"\n✅ Finished collecting cookies. Saved to {COOKIES_JSON_FILE_NAME}")
