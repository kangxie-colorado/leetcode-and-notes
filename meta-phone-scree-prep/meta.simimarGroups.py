"""
should have done this before
union-find


"""

from typing import List


class Solution:
    def numSimilarGroups(self, strs: List[str]) -> int:
        
        def isSimilar(str1, str2):
            diff = 0
            for c1,c2 in zip(str1, str2):
                diff += c1!=c2 
                if diff > 2:
                    return False
            
            return True
        
        grps = [i for i in range(len(strs))]
        def find(x):
            if x != grps[x]:
                grps[x] = find(grps[x])
            return grps[x]

        def union(x,y):
            grps[find(x)]  = grps[find[y]]

        for i in range(len(strs)):
            for j in range(i+1, len(strs)):
                if isSimilar(strs[i], strs[j]):
                    union(i,j)
        
        distintGrps = set()
        for i in range(len(grps)):
            distintGrps.add(find(i))

        return len(distintGrps)

