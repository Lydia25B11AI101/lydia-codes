"""
Program  : 54_api_data_fetcher.py
Title    : REST API Data Fetcher & JSON Processor
Author   : Lydia S. Makiwa  
Date     : 2026-06-01

Description:
    A reusable API client that fetches data from public REST APIs,
    processes JSON responses, and saves results locally.
    Demonstrates error handling, pagination, rate limiting awareness,
    and data transformation — essential for any data engineering
    or full-stack AIML role.
"""

import requests
import json
import time
from datetime import datetime


class APIDataFetcher:
    """
    A general-purpose API client with error handling,
    rate limiting, and data extraction capabilities.
    """
    
    def __init__(self, base_url, headers=None, rate_limit_pause=1.0):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.rate_limit_pause = rate_limit_pause  # seconds between calls
        self.last_call_time = 0
    
    def _respect_rate_limit(self):
        """Pause if we're calling too fast to respect rate limits."""
        elapsed = time.time() - self.last_call_time
        if elapsed < self.rate_limit_pause:
            time.sleep(self.rate_limit_pause - elapsed)
        self.last_call_time = time.time()
    
    def get(self, endpoint, params=None):
        """
        Perform a GET request with error handling.
        Returns parsed JSON data or None on failure.
        """
        self._respect_rate_limit()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.get(
                url, headers=self.headers, params=params, timeout=15
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            print(f"  ⚠ HTTP {response.status_code}: {e}")
            if response.status_code == 429:
                print("    Rate limited! Consider increasing pause time.")
            return None
        except requests.exceptions.ConnectionError:
            print(f"  ⚠ Connection error: Could not reach {url}")
            return None
        except requests.exceptions.Timeout:
            print(f"  ⚠ Timeout: {url} took too long to respond")
            return None
        except json.JSONDecodeError:
            print(f"  ⚠ Invalid JSON response from {url}")
            return None
    
    def fetch_paginated(self, endpoint, params=None, max_pages=3):
        """
        Fetch all pages of results (assumes ?page=N parameter).
        Returns combined list of results.
        """
        params = params or {}
        all_results = []
        
        for page in range(1, max_pages + 1):
            params["page"] = page
            data = self.get(endpoint, params)
            
            if data is None:
                break
            
            # Handle both list and dict-with-results-key responses
            if isinstance(data, list):
                all_results.extend(data)
                if len(data) < 20:  # assume less than page size = last page
                    break
            elif isinstance(data, dict):
                # Try common result keys
                result = (
                    data.get("results") or data.get("data") or
                    data.get("items") or data.get("records")
                )
                if result and isinstance(result, list):
                    all_results.extend(result)
                else:
                    all_results.append(data)
                    break
            else:
                all_results.append(data)
                break
        
        return all_results
    
    def extract_fields(self, items, field_map):
        """
        Extract specific fields from a list of dicts.
        field_map: {output_name: json_path} 
        e.g. {"name": "name", "population": "population"}
        Supports nested paths: "name.first" or ["results", "0", "name"]
        """
        extracted = []
        for item in items:
            record = {}
            for out_name, path in field_map.items():
                value = self._get_nested(item, path)
                record[out_name] = value
            extracted.append(record)
        return extracted
    
    @staticmethod
    def _get_nested(obj, path):
        """Get a nested value using dot notation or list of keys."""
        if isinstance(path, str):
            keys = path.split(".")
        else:
            keys = path
        
        current = obj
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key)
            elif isinstance(current, (list, tuple)):
                try:
                    current = current[int(key)]
                except (ValueError, IndexError):
                    return None
            else:
                return None
        return current
    
    def save_json(self, data, filename):
        """Save data to a JSON file."""
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  💾 Saved {len(data)} records to {filename}")


# ===== DEMO =====
if __name__ == "__main__":
    print("=" * 55)
    print("   REST API DATA FETCHER — DEMO")
    print("   Fetching from real public APIs")
    print("=" * 55)
    
    # Demo 1: Fetch countries from REST Countries API
    print("\n📡 Fetching countries from REST Countries API...")
    fetcher = APIDataFetcher("https://restcountries.com/v3.1")
    countries = fetcher.get("all", params={"fields": "name,population,region,capital"})
    
    if countries:
        field_map = {
            "country": "name.common",
            "capital": "capital.0",
            "region": "region",
            "population": "population"
        }
        extracted = fetcher.extract_fields(countries[:10], field_map)
        print(f"\n   🌍 Sample countries (showing first 10 of {len(countries)}):")
        for i, c in enumerate(extracted, 1):
            cap = c["capital"] or "N/A"
            pop = f"{c['population']:,}" if c["population"] else "Unknown"
            print(f"   {i:2d}. {c['country']:25s} | {c['region']:15s} | Pop: {pop}")
    
    # Demo 2: Fetch JSONPlaceholder posts
    print("\n📡 Fetching sample posts from JSONPlaceholder...")
    fetcher2 = APIDataFetcher("https://jsonplaceholder.typicode.com")
    posts = fetcher2.get("posts", params={"_limit": 5})
    
    if posts:
        print("\n   📝 Recent posts:")
        for post in posts[:5]:
            print(f"   [{post['id']:3d}] {post['title'][:50]}...")
    
    # Demo 3: Paginated fetch
    print("\n📡 Testing paginated fetch (first 2 pages)...")
    paginated = fetcher2.fetch_paginated("posts", max_pages=2)
    print(f"   Fetched {len(paginated)} total posts across pages")
    
    print("\n💡 Try extending this: fetch from GitHub API, weather APIs,")
    print("   or public transport APIs for your own data project!")
