from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
import json
import argparse
parser = argparse.ArgumentParser(description="Scrape cookies in desktop or mobile mode.")
parser.add_argument("--mobile", action="store_true", help="Run browser in mobile emulation mode")
args = parser.parse_args()
NUM_WEBSITES = 10
IS_MOBILE = args.mobile

if IS_MOBILE:
    COOKIES_JSON_FILE_NAME = "mobile_cookies.json"
else:
    COOKIES_JSON_FILE_NAME = "website_cookies.json"


def get_cookies(url: str):
    # Set up Chrome options for headless mode
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    if IS_MOBILE:
        options.add_argument(
            "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        )

    # Initialize WebDriver with the options
    driver = webdriver.Chrome(options=options)
    """Retrieve cookies from the browser as a set of (name, value) tuples"""
    try:
        driver.get(url)
        cookies = driver.get_cookies()
        return cookies
    except Exception as e:
        print(f"Error occurred")
    finally:
        driver.quit()


df = pd.read_csv("open-cookie-database.csv")
name_to_category = dict()
to_delete_arr = set()

for idx, row in df.iterrows():
    name = row["Cookie / Data Key name"]

    category = row["Category"]
    if name in name_to_category:
        og_cat = name_to_category[name]
        if category != og_cat:
            to_delete_arr.add(name)
    name_to_category[name] = row["Category"]

for to_delete in to_delete_arr:
    name_to_category.pop(to_delete)

with open("top-10000-domains", "r") as file:
    website_arr = file.readlines()

website_to_cookies = dict()
for website in website_arr[:NUM_WEBSITES]:
    cookies = get_cookies("https://www." + website)
    website_to_cookies[website] = cookies


for website, cookies_arr in website_to_cookies.items():
    if not cookies_arr:
        continue
    for cookie in cookies_arr:
        name = cookie["name"]
        cookie["classification"] = name_to_category.get(name)

with open(COOKIES_JSON_FILE_NAME, "w") as file:
    json.dump(website_to_cookies, file, indent=4)
