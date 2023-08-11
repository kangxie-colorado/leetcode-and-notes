"""
only 26 chars
"""
from collections import defaultdict
from typing import List


class Solution:
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        charsOrder = defaultdict(int)
        for i,c in enumerate(order):
            # 1 to 26, leave 0 to empty
            charsOrder[c] = i+1

        def wordsInOrder(w1,w2):
            # find first different char
            i=j=0
            while i<len(w1) and j<len(w2) and w1[i] == w2[j]:
                i+=1
                j+=1
                
            c1 = charsOrder[w1[i]] if i<len(w1) else 0
            c2 = charsOrder[w2[j]] if j<len(w2) else 0
            return c1<=c2

        for i in range(1, len(words)):
            w1, w2 = words[i-1], words[i]
            if not wordsInOrder(w1, w2):
                return False
        
        return True