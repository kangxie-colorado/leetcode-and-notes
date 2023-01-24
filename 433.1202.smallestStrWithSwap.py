"""
https://leetcode.com/problems/smallest-string-with-swaps/?envType=study-plan&id=graph-ii

this is similar problem to a previous problem 1061
twist is the sort is by char, the swap is shown as idx..

not super hard (when I am in a streak of union-find)
"""


from collections import defaultdict
from typing import List


class Solution:
    def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
        roots = {} # mapping char:char

        def find(c):
            roots.setdefault(c,c)
            if roots[c] != c:
                roots[c] = find(roots[c])
            return roots[c]
        
        def union(c1,c2):
            r1,r2 = find(c1), find(c2) 
            if r1<r2:
                roots[r2] = roots[r1]
            else:
                roots[r1] = roots[r2]
        
        for i,j in pairs:
            union(s[i],s[j])
        
        res = []
        for c in s:
            res.append(find(c))
        return "".join(res)

"""
wait..

why cannot I just walk thru the pairs and swap to smaller string?
will it work?

I guess not, but interesting to find out

back from naive failure.. but quickly failed at 
"dcab"
[[0,3],[1,2]]
output: baad
expect: bacd

it is swap, not to get the equivilent string

okay.. let me see 
so maybe I get all the sungroups and sorted it?
"""


class Solution:
    def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
        chars = list(s)
        for i,j in pairs:
            if i>j:
                i,j = j,i
            
            if chars[i] > chars[j]:
                chars[i],chars[j] = chars[j], chars[i]
        return "".join(chars)

"""
okay.. it failed quickly

"dcab"
[[0,3],[1,2],[0,2]]

back to union find 



back from naive failure.. but quickly failed at 
"dcab"
[[0,3],[1,2]]
output: baad
expect: bacd

it is swap, not to get the equivilent string

okay.. let me see 
so maybe I get all the sungroups and sorted it?

looks like I should work on index to union-find.. and sort that sub-sequence
"""


class Solution:
    def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
        roots = [i for i in range(len(s))]

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x, y):
            roots[find(x)] = roots[find(y)]

        for i, j in pairs:
            union(i,j)

        # sort the sub-components 
        # first: I need to get those sub-components?
        rootToSubseq = defaultdict(list)
        for i in range(len(s)):
            r = find(i)
            rootToSubseq[r].append((s[i], i))


        res = [""]*len(s)
        for r,subseq in rootToSubseq.items():
            indexs = [ss[1] for ss in subseq]
            strs = [ss[0] for ss in subseq]
            strs.sort()
            for c,idx in zip(strs, indexs):
                res[idx] = c

        return "".join(res)


"""
Runtime: 1292 ms, faster than 31.69% of Python3 online submissions for Smallest String With Swaps.
Memory Usage: 50.4 MB, less than 67.42% of Python3 online submissions for Smallest String With Swaps.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.smallestStringWithSwaps(s = "dcab", pairs = [[0,3],[1,2]]))
    print(s.smallestStringWithSwaps(s = "dcab", pairs = [[0,3],[1,2],[0,2]]))
    print(s.smallestStringWithSwaps(s = "cba", pairs = [[0,1],[1,2]]))