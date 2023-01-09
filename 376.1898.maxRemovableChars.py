"""
https://leetcode.com/problems/maximum-number-of-removable-characters/?envType=study-plan&id=binary-search-ii


not sure how I was able to do it before
maybe it was because I was in some special state.

now I feel it is not that easy
but I still can see it seems like a binary search problem
"""


from typing import List


class Solution:
    def maximumRemovals(self, s: str, p: str, removable: List[int]) -> int:

        def valid(k):
            # removing k chars and check if s still contains p
            toRemove = set(removable[:k])
            j = 0
            for i, c in enumerate(s):
                if i in toRemove:
                    continue
                if c == p[j]:
                    # if I match a char in p
                    j += 1
                if j == len(p):
                    # if it already matchs all p, return early
                    break
            # at the end check if all the chars in p are matched
            return j == len(p)

        l, r = 0, len(removable)
        while l < r:
            m = r-(r-l)//2

            if valid(m):
                l = m
            else:
                r = m - 1
        return l

"""
Runtime: 2843 ms, faster than 91.59% of Python3 online submissions for Maximum Number of Removable Characters.
Memory Usage: 30.2 MB, less than 77.95% of Python3 online submissions for Maximum Number of Removable Characters.

checked previous submissions, I think code is better 
"""
    
if __name__ == '__main__':
    print(Solution().maximumRemovals( s = "abcacb", p = "ab", removable = [3,1,0]))