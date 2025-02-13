import requests
from bs4 import BeautifulSoup

def extract_article_links(url):
    """Extracts article links from a given goo blog archive page.

    Args:
        url: The URL of the archive page.

    Returns:
        A list of absolute article URLs, or an empty list if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors (404, 500, etc.)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with class "entry-body-text"
        entry_body_div = soup.find('div', class_='entry-body-text')

        if not entry_body_div:
            print("Could not find the entry-body-text div.")
            return []

        # Find the <ul> list within that div
        ul_element = entry_body_div.find('ul')

        if not ul_element:
            print("Could not find the <ul> element.")
            return []

        all_links = []
        # Iterate through the <li> elements within the <ul>
        for li_element in ul_element.find_all('li'):
            # Find the <a> tag within the <li>
            a_tag = li_element.find('a')
            if a_tag and 'href' in a_tag.attrs:  # Check if the 'href' attribute exists
                link = a_tag['href']
                # Make the link absolute (in case it's relative)
                absolute_link = requests.compat.urljoin(url, link)
                all_links.append(absolute_link)

        return all_links

    except requests.exceptions.RequestException as e:
        print(f"Error fetching or parsing URL: {e}")
        return []

# --- Example Usage ---
archive_url = "https://blog.goo.ne.jp/ishiseiji/arcv/"
article_links = extract_article_links(archive_url)

if article_links:
    print("Extracted Article Links:")
    for link in article_links:
        print(link)
    print(f"\nTotal Links Found: {len(article_links)}")
else:
    print("No links extracted.")