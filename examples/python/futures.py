#!/usr/bin/env python3
import concurrent.futures
import random
import time

URLS = ["apple", "banana", "orange", "grape"]


def long_task(url):
    print("running " + str(url))
    time.sleep(random.randint(0, 5))
    print("finished " + str(url))
    return "i finished " + str(url)


# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(long_task, url): url for url in URLS}
    print("i have submitted them all " + str(future_to_url.keys()))
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print(f"{url!r} generated an exception: {exc}")
        else:
            print("future succeeded with " + str(data))
