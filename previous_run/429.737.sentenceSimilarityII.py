"""
https://leetcode.com/problems/sentence-similarity-ii/?envType=study-plan&id=graph-ii

union find - very obvious 
one little conversion to do is to map word to a sequence maybe 
"""


from typing import List


class Solution:
    def areSentencesSimilarTwo(self, sentence1: List[str], sentence2: List[str], similarPairs: List[List[str]]) -> bool:
        if len(sentence1) != len(sentence2):
            return False

        # 1 <= sentence1.length, sentence2.length <= 1000
        # 0 <= similarPairs.length <= 2000
        # not a very big one
        roots = [i for i in range(len(similarPairs)*2)]

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x, y):
            roots[find(x)] = roots[find(y)]

        seq = 0
        words = {}  # mapping word to seq
        for w1, w2 in similarPairs:
            if w1 not in words:
                words[w1] = seq
                seq += 1
            if w2 not in words:
                words[w2] = seq
                seq += 1

            union(words[w1], words[w2])

        for w1, w2 in zip(sentence1, sentence2):
            if w1!=w2 and (w1 not in words or w2 not in words or find(words[w1]) != find(words[w2])):
                return False

        return True

"""
Runtime: 619 ms, faster than 41.12% of Python3 online submissions for Sentence Similarity II.
Memory Usage: 15.6 MB, less than 89.14% of Python3 online submissions for Sentence Similarity II.
"""
