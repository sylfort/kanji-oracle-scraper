import http.client
import json
import time
import random
import re
from bs4 import BeautifulSoup
import requests

base_url = "https://blog.goo.ne.jp/ishiseiji/arcv/"
all_article_data = []  # List to store dictionaries of article data
total_pages = 50  # Since we know there are 50 pages

# --- ScrapingAnt API Key and Settings ---
scrapingant_api_key = "07c0cc0bb3144fd1bd66aaeb7438c78b"  # Replace with your actual API key
proxy_type = "residential"
proxy_country = "JP"
use_browser_rendering = False


def fetch_page_via_scrapingant(url):
    """Fetches a page using the ScrapingAnt API."""
    conn = http.client.HTTPSConnection("api.scrapingant.com")
    encoded_url = requests.utils.quote(url, safe='')
    api_url = (f"/v2/general?url={encoded_url}&x-api-key={scrapingant_api_key}"
               f"&proxy_type={proxy_type}&proxy_country={proxy_country}&browser={str(use_browser_rendering).lower()}")

    print(f"Fetching via ScrapingAnt: {url}")
    try:
        conn.request("GET", api_url)
        res = conn.getresponse()
        data = res.read()
        if res.status == 200:
            return data.decode("utf-8")
        else:
            print(f"ScrapingAnt Error: Status {res.status}, Reason: {res.reason}")
            return None
    except Exception as e:
        print(f"Error fetching with ScrapingAnt: {e}")
        return None


def parse_html_for_article_data(html_content):
    """Parses the HTML content and extracts article data."""
    soup = BeautifulSoup(html_content, 'html.parser')
    article_data = []
    list_items = soup.select('.entry-body .entry-body-text ul li')

    for li in list_items:
        link_element = li.select_one('.mod-arcv-tit a')
        if not link_element:
            continue
        href = link_element['href']
        title = link_element.text.strip()
        date_match = re.search(r'\((\d{4}年\d{2}月\d{2}日)', str(li))
        date = date_match.group(1) if date_match else None

        article_data.append({'href': href, 'title': title, 'date': date})
    return article_data


# --- Main Scraping Loop (using a for loop) ---
for page_num in range(32, total_pages + 1):  # Iterate from 1 to 50 (inclusive)
    url = f"{base_url}?page={page_num}&c=&st=0"
    html_content = fetch_page_via_scrapingant(url)

    if html_content:
        article_data_page = parse_html_for_article_data(html_content)
        all_article_data.extend(article_data_page)
    else:
        print(f"Failed to fetch page {page_num}. Stopping.")
        break  # Stop if ScrapingAnt fails

    sleep_time = random.uniform(2, 10)
    print(f"Sleeping for {sleep_time:.2f} seconds...")
    time.sleep(sleep_time)


# --- Save to JSON ---
with open("article_data3.json", "w", encoding="utf-8") as f:
    json.dump(all_article_data, f, indent=4, ensure_ascii=False)

print(f"\nFound data for {len(all_article_data)} articles. Saved to article_data.json")