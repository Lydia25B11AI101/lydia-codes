# Python Program 26: Web Scraping with BeautifulSoup
# Author: Lydia S. Makiwa
# Description: Scrapes a webpage and extracts structured data

import urllib.request
from html.parser import HTMLParser

class HeadingParser(HTMLParser):
    """Extracts headings and links from HTML."""
    def __init__(self):
        super().__init__()
        self.headings = []
        self.links    = []
        self._in_heading = False
        self._current_tag = ""

    def handle_starttag(self, tag, attrs):
        if tag in ("h1","h2","h3"):
            self._in_heading  = True
            self._current_tag = tag
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value and value.startswith("http"):
                    self.links.append(value)

    def handle_endtag(self, tag):
        if tag in ("h1","h2","h3"):
            self._in_heading = False

    def handle_data(self, data):
        if self._in_heading and data.strip():
            self.headings.append((self._current_tag.upper(), data.strip()))


def scrape_page(url):
    print(f"Fetching: {url}\n")
    try:
        req  = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        parser = HeadingParser()
        parser.feed(html)

        print(f"Found {len(parser.headings)} headings:")
        for tag, text in parser.headings[:10]:
            indent = "  " if tag == "H1" else "    " if tag == "H2" else "      "
            print(f"{indent}[{tag}] {text[:70]}")

        print(f"\nFound {len(parser.links)} external links (first 5):")
        for link in parser.links[:5]:
            print(f"  🔗 {link[:80]}")

    except Exception as e:
        print(f"Error: {e}")

# Demo — scrape Python docs homepage
scrape_page("https://www.python.org")
