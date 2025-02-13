import requests
from bs4 import BeautifulSoup
import time
import random
import json  # For saving to JSON if direct scraping fails

base_url = "https://blog.goo.ne.jp/ishiseiji/arcv/"
all_article_links = []
max_pages_to_check = 5  # Start small for testing

# --- More Comprehensive Headers (Try these) ---
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'Accept-Language': 'en-US,en;q=0.9',  # Or your preferred language
#     'Accept-Encoding': 'gzip, deflate, br', # Important
#     'Referer': 'https://blog.goo.ne.jp/ishiseiji/',
#     'Connection': 'keep-alive',
#     'Upgrade-Insecure-Requests': '1',
#     'Cache-Control': 'max-age=0'
# }
headers={"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0"}

session = requests.Session()
session.headers.update(headers)

def fetch_and_parse(page_num):
    """Fetches a page, parses it, and extracts article links.
       Returns a list of links, or None if there's an error.
    """
    url = f"{base_url}?page={page_num}&c=&st=0"
    print(f"Fetching page: {url}")

    try:
        response = session.get(url)
        response.raise_for_status()

        print(f"Status Code: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        article_links = []
        article_entries = soup.find_all('div', class_='blogbody')
        for entry in article_entries:
            title_element = entry.find('h2')
            if title_element:
                link_element = title_element.find('a')
                if link_element:
                    article_links.append(link_element['href'])
        return article_links

    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_num}: {e}")
        return None

# --- Main Scraping Loop ---
page_num = 1
while page_num <= max_pages_to_check:
    links = fetch_and_parse(page_num)

    if links is not None:
        all_article_links.extend(links)
        next_page_link = BeautifulSoup(requests.get(f"{base_url}?page={page_num}&c=&st=0").text, 'html.parser').find('a', string='次>') #check if next page exists, even after a 403.
        if not next_page_link:
          print("No next page found. Stopping.")
          break

    else:  # Error occurred
        # --- Fallback Plan (Manual Extraction) ---
        print("Direct scraping failed.  Attempting manual extraction from saved HTML.")
        print("Please manually visit the pages, save the HTML as page_1.html, page_2.html, etc.,")
        print("in the same directory as this script. Then, run the manual extraction section below.")
        break  # Exit the scraping loop

    page_num += 1
    sleep_time = random.uniform(3, 7)
    print(f"Sleeping for {sleep_time:.2f} seconds...")
    time.sleep(sleep_time)
# --- Manual Extraction (if direct scraping fails) ---
#  Uncomment this section *only* if the above scraping loop fails
#  and you've manually saved the HTML files.

manual_extraction = False  # Set to True after manually saving files
if manual_extraction:
    all_article_links_manual = []
    for i in range(1, max_pages_to_check + 1):
        try:
            with open(f"page_{i}.html", "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f, 'html.parser')
                article_entries = soup.find_all('div', class_='blogbody')
                for entry in article_entries:
                    title_element = entry.find('h2')
                    if title_element:
                        link_element = title_element.find('a')
                        if link_element:
                            all_article_links_manual.append(link_element['href'])
        except FileNotFoundError:
            print(f"File page_{i}.html not found. Stopping manual extraction.")
            break
    print("\nManually Extracted Links:")
    for link in all_article_links_manual:
        print(link)
    print(f"Total articles found (manually): {len(all_article_links_manual)}")

    #Optionally save this info to a json file
    with open("article_links.json", "w") as f:
      json.dump(all_article_links_manual, f, indent=4)

else:
    print("\nFound Article Links (Direct Scraping):")
    for link in all_article_links:
        print(link)

    print(f"\nTotal articles found (direct): {len(all_article_links)}")
    #Optionally save this info to a json file
    with open("article_links.json", "w") as f:
      json.dump(all_article_links, f, indent=4)