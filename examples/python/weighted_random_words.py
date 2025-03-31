#!/usr/bin/env python3

import random
import time

example_list = [("apple", 5), ("banana", 2), ("orange", 9), ("grape", 1)]


class Solution:
    def __init__(self, words):
        i = 0
        self.items = []
        for word, weight in words:
            i += weight
            self.items.append((i, word))
        self.max = i
        print(self.items)

    def get_random_word(self):
        r = random.randint(0, self.max)
        print(r)
        left = 0
        right = len(self.items)
        while True:
            mid = int((left + right) / 2)
            print(f"{left} {mid} {right}")
            if r < self.items[mid][0]:
                right = mid
                if left == mid:
                    return self.items[left][1]
            else:
                left = mid
                if right == mid:
                    return self.items[left][1]
            time.sleep(1)


s = Solution(example_list)
print(s.get_random_word())
