from collections import defaultdict
from functools import cache
from typing import List


class WordDistance:

    def __init__(self, wordsDict: List[str]):
        self.words = defaultdict(set)
        for idx,word in enumerate(wordsDict):
            self.words[word].add(idx)

    @cache 
    def shortest(self, word1: str, word2: str) -> int:
        positions = sorted(list(self.words[word1].union(self.words[word2])))

        res = float('inf')
        for i in range(1, len(positions)):
            pos1,pos2 = positions[i-1], positions[i]
            if (pos1 in self.words[word1] and pos2 in self.words[word1]) or (pos1 in self.words[word2] and pos2 in self.words[word2]):
                continue

            res = min(res, pos2-pos1)
        
        return res


"""
Runtime: 115 ms, faster than 76.01% of Python3 online submissions for Shortest Word Distance II.
Memory Usage: 22.7 MB, less than 6.36% of Python3 online submissions for Shortest Word Distance II.

okay.. maybe the sort is unnecessary
there are by themselves naturally sorted already
"""


class WordDistance:

    def __init__(self, wordsDict: List[str]):
        self.words = defaultdict(list)
        for idx, word in enumerate(wordsDict):
            self.words[word].append(idx)

    @cache
    def shortest(self, word1: str, word2: str) -> int:
        pos1s = self.words[word1]
        pos2s = self.words[word2]

        i=j=0

        res = float('inf')
        while i<len(pos1s) and j<len(pos2s):
            pos1,pos2 = pos1s[i], pos2s[j]
            res = min(res, abs(pos2-pos1))
            if pos1<pos2:
                i+=1
            else:
                j+=1
        

        return res

"""
Runtime: 108 ms, faster than 82.80% of Python3 online submissions for Shortest Word Distance II.
Memory Usage: 21.9 MB, less than 31.21% of Python3 online submissions for Shortest Word Distance II.
"""