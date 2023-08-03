"""
https://leetcode.com/problems/bulls-and-cows/


I just find it easy to go thru twice
1. take care of bulls
2. take care of cows

mix them together complicated things somehow...

"""

from collections import Counter


class Solution:
    def getHint(self, secret: str, guess: str) -> str:
        bulls = cows = 0
        C = Counter(secret)

        for i, c in enumerate(guess):
            if secret[i] == c:
                # bull
                bulls += 1
                C[c] -= 1
        for i, c in enumerate(guess):
            if secret[i] != c and C[c] > 0:
                # cow
                cows += 1
                C[c] -= 1

        return f"{bulls}A{cows}B"
