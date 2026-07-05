from bs4 import BeautifulSoup
import requests
import time
import threading

def fetch_and_get_length(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"Length of text from {url}: {len(soup.get_text())}")



urls = ["https://example.com", "https://lipsum.com", "https://python.org"]

#without multi threading it took 3.22 seconds
#with threading it took 1.76 seconds

if __name__ == "__main__":
    threads = []
    t = time.time()
    for url in urls:
        thead  = threading.Thread(target=fetch_and_get_length, args=(url,))
        threads.append(thead)
        thead.start()
    for thread in threads:
        thread.join()   
    print("Time taken without threading: ", time.time() - t)