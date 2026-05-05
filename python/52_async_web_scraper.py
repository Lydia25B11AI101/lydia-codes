# Program Title: Async Web Scraper with asyncio & urllib
# Author: Lydia S. Makiwa
# Date: 2026-05-05
# Description: Demonstrates asynchronous HTTP requests using asyncio
#              and concurrent.futures. Shows how to scrape multiple URLs
#              in parallel — a key skill for data engineering roles.

import asyncio
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import time

class TitleParser(HTMLParser):
    """Extract <title> tag from HTML."""
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title    = ""
    def handle_starttag(self, tag, attrs):
        if tag == "title": self.in_title = True
    def handle_data(self, data):
        if self.in_title: self.title += data
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False

def fetch_url(url):
    """Fetch a single URL and return (url, title, status)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            html  = resp.read(4096).decode("utf-8", errors="ignore")
            p     = TitleParser()
            p.feed(html)
            title = p.title.strip() or "(no title)"
            return url, title, resp.status
    except urllib.error.HTTPError as e:
        return url, f"HTTP Error {e.code}", e.code
    except Exception as e:
        return url, f"Error: {e}", 0

async def scrape_async(urls):
    """Run all fetches concurrently using a thread pool."""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=10) as pool:
        tasks   = [loop.run_in_executor(pool, fetch_url, u) for u in urls]
        results = await asyncio.gather(*tasks)
    return results

# ─── Demo ───
URLS = [
    "https://www.python.org",
    "https://github.com",
    "https://www.wikipedia.org",
    "https://httpbin.org",
    "https://www.bbc.com",
]

print("Fetching pages asynchronously...")
print(f"URLs to scrape: {len(URLS)}\n")

start  = time.time()
results = asyncio.run(scrape_async(URLS))
elapsed = time.time() - start

print(f"{'-'*60}")
print(f"{'URL':<35} {'STATUS':<8} TITLE")
print(f"{'-'*60}")
for url, title, status in results:
    short = url.replace("https://","").replace("www.","")[:32]
    print(f"{short:<35} {status:<8} {title[:45]}")

print(f"\n⏱  Total time: {elapsed:.2f}s for {len(URLS)} URLs (async concurrent)")
