"""
https://leetcode.com/problems/similar-string-groups/?envType=study-plan&id=graph-ii

if I don't know union find, it is more difficult
now so this becomes
if two string are similar, union them.. 

let me see if it passes
"""


from typing import List


class Solution:
    def numSimilarGroups(self, strs: List[str]) -> int:
        roots = {}

        def find(s):
            roots.setdefault(s,s)
            if roots[s] != s:
                roots[s] = find(roots[s])
            return roots[s]
        
        def union(s1,s2):
            roots[find(s1)] = roots[find(s2)]
        
        def similar(s1,s2):
            diffs = 0
            for c1,c2 in zip(s1,s2):
                if c1 != c2:
                    diffs += 1
                
                if diffs>2:
                    return False

            return diffs==0 or diffs == 2 

        # j also starts with i, union with itself
        # for those to be a group alone
        for i in range(len(strs)):
            for j in range(i, len(strs)):
                s1,s2 = strs[i], strs[j]
                if similar(s1,s2):
                    union(s1, s2)
        
        rootSet = set()
        for s in roots:
            rootSet.add(find(s))
        return len(rootSet)

"""
Runtime: 6792 ms, faster than 8.52% of Python3 online submissions for Similar String Groups.
Memory Usage: 15.1 MB, less than 6.32% of Python3 online submissions for Similar String Groups.

Runtime: 3313 ms, faster than 34.07% of Python3 online submissions for Similar String Groups.
Memory Usage: 15.1 MB, less than 6.32% of Python3 online submissions for Similar String Groups.

adding this 
                if diffs>2:
                    return False
Runtime: 298 ms, faster than 87.36% of Python3 online submissions for Similar String Groups.
Memory Usage: 15.1 MB, less than 6.32% of Python3 online submissions for Similar String Groups.

"""
    
if __name__ == '__main__':
    s = Solution()
    print(s.numSimilarGroups(strs = ["tars","rats","arts","star"]))