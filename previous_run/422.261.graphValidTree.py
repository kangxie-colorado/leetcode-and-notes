"""
https://leetcode.com/problems/graph-valid-tree/

okay starting the graph study plan
and a new problem greets me 

so basically this is cycle detection?
looks like it 
"""


from collections import defaultdict
from typing import List


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        adjSets = defaultdict(set)
        # 1. build the adjacent sets
        for s,e in edges:
            adjSets[s].add(e)
        
        # 2. randomly start from a node, see if it can walk to all the nodes without
        # running into itself 
        # actually, maybe this is a union find problem but dfs could do it anyway
        # just keep path and visited states
        def cycle(node, parent, path):
            if node in path:
                return True
            
            path.add(node)
            for nei in adjSets[node]:
                if nei != parent and cycle(nei, node, path):
                    return True
                
            return False 
        
        return not cycle(edges[0][0], -1, set())

"""
4
[[0,1],[2,3]]

okay.. disconnected graphs
uhg.. if it is disconnected graph, it cannot be a tree
but two trees 
"""


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if not edges:
            return n==1
        adjSets = defaultdict(set)
        # 1. build the adjacent sets
        for s, e in edges:
            adjSets[s].add(e)
            adjSets[e].add(s)

        # 2. randomly start from a node, see if it can walk to all the nodes without
        # running into itself
        # actually, maybe this is a union find problem but dfs could do it anyway
        # just keep path and visited states
        visited = set()
        def cycle(node, parent, path):
            if node in path:
                return True

            path.add(node)
            for nei in adjSets[node]:
                if nei != parent and cycle(nei, node, path):
                    return True

            visited.add(node)
            return False

        return not cycle(edges[0][0], -1, set()) and len(visited)==n

"""
1 [] - true
2 [] - false

special hanlding 
        if not edges:
            return n==1


Runtime: 144 ms, faster than 41.28% of Python3 online submissions for Graph Valid Tree.
Memory Usage: 18 MB, less than 7.97% of Python3 online submissions for Graph Valid Tree.

let me see, if I use union find
the cycle can be detected by find(x)==find(y)

but the disconnected how to detect?
like if there are multiple roots? (o(n))
give a try
"""


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if not edges:
            return n == 1

        roots = [i for i in range(n)]

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]
        
        def union(x,y):
            # it needs to be find(x) 
            # union their root
            roots[find(x)] = find(y)
        
        for n1,n2 in edges:
            if find(n1) == find(n2):
                return False
            union(n1,n2)
        
        uniqRoots = set()
        for r in roots:
            root = find(r)
            if uniqRoots and root not in uniqRoots:
                return False
            uniqRoots.add(root)
        return True

"""
Runtime: 189 ms, faster than 35.40% of Python3 online submissions for Graph Valid Tree.
Memory Usage: 16.5 MB, less than 32.62% of Python3 online submissions for Graph Valid Tree.
"""


class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n-1:
            return False

        roots = [i for i in range(n)]

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x, y):
            roots[find(x)] = find(y)

        for n1, n2 in edges:
            if find(n1) == find(n2):
                return False
            union(n1, n2)

        uniqRoots = set()
        for r in roots:
            root = find(r)
            if uniqRoots and root not in uniqRoots:
                return False
            uniqRoots.add(root)
        return True

"""
a better way to deal with the edge case

        if len(edges) != n-1:
            return False
    this fails, must return false
    this passes, could be a tree 
works on union-find, but not on dfs method (I mean easily)
"""

if __name__ == '__main__':
    s = Solution()
    print(s.validTree(5,[[0,1],[0,2],[0,3],[1,4]]))