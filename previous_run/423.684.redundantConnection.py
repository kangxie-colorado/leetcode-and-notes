"""
https://leetcode.com/problems/redundant-connection/?envType=study-plan&id=graph-ii

now I should be able to this easy
"""


from typing import List


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        roots = [i for i in range(n+1)]

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]
        
        def union(x,y):
            roots[find(x)] = find(y)
        
        for x,y in edges:
            if find(x) == find(y):
                return [x,y]
            union(x,y)

"""
Runtime: 61 ms, faster than 68.67% of Python3 online submissions for Redundant Connection.
Memory Usage: 14.3 MB, less than 89.98% of Python3 online submissions for Redundant Connection.

there are some subtilities here
 If there are multiple answers, return the answer that occurs last in the input.

this will form a cycle, so removing any edge might work
but it needs to be the last one.. 

the union find will find the first edge that cause this cycle.. and because there are n nodes, n edges
so this edge happens to be the last eligible edge... (in the input)

okay.. since I am done with today's quota..
continue on to those greyed ones...
"""