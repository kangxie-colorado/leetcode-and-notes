"""
with a quick experiment
this world must be built starting from a single char

ab->abc without a won't count
"""

from typing import List


class Solution:
    def longestWord(self, words: List[str]) -> str:
        res = ""
        words = set(words)
        for word in words:
            eligible = True
            for i in range(1,len(word)+1):
                if word[:i] not in words:
                    eligible = False
                    break
            if eligible and (len(word)>len(res) or (len(word)==len(res) and word<res)):
                res = word
        
        return res

                    
                
        