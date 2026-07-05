from concurrent.futures import ThreadPoolExecutor
import time
import requests
from bs4 import BeautifulSoup

def fetch_and_get_length(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return f"Length of text from {url}: {len(soup.get_text())}"


urls = ["https://example.com", "https://lipsum.com", "https://python.org"]

#took 1.83
if __name__ == "__main__":
    start_time = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=3) as executor:
       results = executor.map(fetch_and_get_length, urls)
    for result in results:
        print(result)
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")