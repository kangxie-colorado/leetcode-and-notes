
from typing import List


class Solution:
    def largeGroupPositions(self, s: str) -> List[List[int]]:
        
        res = []
        i,j = 0,1

        while j<len(s):
            if s[j]!=s[i]:
                if j-i>=3:
                    res.append([i,j-1])
                i=j
            j+=1

        if j-i>=3:
            res.append([i,j-1])

        return res

            