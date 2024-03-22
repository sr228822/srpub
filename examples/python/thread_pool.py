#!/usr/bin/env python3

import random, time
from contextlib import closing

import concurrent.futures


# called by each thread
def get_url(url):
    delay = 4 + int(random.random() * 3)
    print(f"starting {url} sleep {delay}")
    time.sleep(delay)
    print(f"finished {url}")
    return f"result {url}"


theurls = ["http://google.com", "http://yahoo.com", "http://nytimes.com"]

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in theurls:
            futures.append(executor.submit(get_url, url=url))
        for future in concurrent.futures.as_completed(futures):
            print(future.result())
