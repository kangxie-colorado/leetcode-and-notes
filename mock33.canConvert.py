from collections import defaultdict


class Solution:
    def canConvert(self, str1: str, str2: str) -> bool:
        if str1 == str2:
            return True
        
        charMap1 = {}
        charMap2 = defaultdict(set)
        
        for c1,c2 in zip(str1, str2):
            if c1 in charMap1 and charMap1[c1] != c2:
                return False
            charMap1[c1] = c2 
            charMap2[c2].add(c1)

        wildcard = set()
        for i in range(26):
            c = chr(ord('a')+i)
            wildcard.add(c)

        for c2,lst in charMap2.items():
            if len(lst) == 1:
                wildcard.remove(c2)                        
        
        return len(wildcard)
