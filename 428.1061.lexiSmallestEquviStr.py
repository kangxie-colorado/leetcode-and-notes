"""
https://leetcode.com/problems/lexicographically-smallest-equivalent-string/?envType=study-plan&id=graph-ii

on a streak of union find, so I know this is a union find problem
and looks like to get to the lexi smallest, I just store the smaller number as the root
"""


class Solution:
    def smallestEquivalentString(self, s1: str, s2: str, baseStr: str) -> str:
        roots = [i for i in range(26)]

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]
        
        def union(x,y):
            xRoot,yRoot = find(x),find(y)
            # simply converge to the smaller char
            if xRoot < yRoot:
                roots[yRoot] = roots[xRoot]
            else:
                roots[xRoot] = roots[yRoot]
        
        for c1,c2 in zip(s1,s2):
            if c1!=c2:
                # union a to a.. might be a problem 
                # at least, don't waste it
                union(ord(c1)-ord('a'),ord(c2)-ord('a'))
        
        res = []
        for c in baseStr:
            res.append(chr(find(ord(c)-ord('a'))+ord('a')))
        
        return "".join(res)

"""
Runtime: 48 ms, faster than 34.28% of Python3 online submissions for Lexicographically Smallest Equivalent String.
Memory Usage: 13.9 MB, less than 88.68% of Python3 online submissions for Lexicographically Smallest Equivalent String.

Runtime: 34 ms, faster than 94.83% of Python3 online submissions for Lexicographically Smallest Equivalent String.
Memory Usage: 13.9 MB, less than 88.68% of Python3 online submissions for Lexicographically Smallest Equivalent String.
"""

if __name__ == '__main__':
    sol = Solution()
    s1= "dfeffdfafbbebbebacbbdfcfdbcacdcbeeffdfebbdebbdafff"
    s2 = "adcdfabadbeeafeabbadcefcaabdecabfecffbabbfcdfcaaae"
    baseStr = "myickvflcpfyqievitqtwvfpsrxigauvlqdtqhpfugguwfcpqv"
    print(sol.smallestEquivalentString(s1, s2, baseStr))