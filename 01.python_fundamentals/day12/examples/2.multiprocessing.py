from bs4 import BeautifulSoup
import requests
import time
import multiprocessing

def fetch_and_get_length(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"Length of text from {url}: {len(soup.get_text())}")



urls = ["https://example.com", "https://lipsum.com", "https://python.org"]


#with multi processing it took 2.1 seconds

if __name__ == "__main__":
    processes = []
    t = time.time()
    for url in urls:
        process  = multiprocessing.Process(target=fetch_and_get_length, args=(url,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()   
    print("Time taken with multiprocessing: ", time.time() - t)