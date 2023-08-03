"""
https://leetcode.com/problems/redundant-connection-ii/?envType=study-plan&id=graph-ii

hmm... interesting?
directed graph.. 

so the union-find has a fix direction
but cannot be that eay????

let me get started first 
"""


from collections import defaultdict
from typing import List


class Solution:
    def findRedundantDirectedConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        roots = [i for i in range(n+1)]

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x, y):
            roots[find(x)] = find(y)

        for p,c in edges:
            if find(c) == find(p):
                return [p,c]
            union(c,p)

"""
failed at 
[[2,1],[3,1],[4,2],[1,4]]

ok... the algorithm above can only remove the cycle
but cannot make it a valid tree yet

4->2->1<-3
^     |
|_____|

the cycle can be eliminated by removing 1,4
but the left things is like this 
4->2->1<-3

not a tree at all
so I guess we'd use this rule: plus every node has exactly one parent, except for the root node which has no parents.

so I guess I can still detect the cycle nodes [4,2,1]
so maybe this ain't a union find problem
don't get tangled by that thought at least 

with that in mind, let me continue thinking laverage union-find a bit
lets see.. this union find could help me identify the cycle 

when x,y forms a cycle... I can tell the cycle is formed by 4,2,1.. then I break one such edge to make it a tree 

nah.. the logic is total wrong
it will union 2 to 3.. after [2,1],[3,1]

okay.. <<<<<< try other ways >>>>>>
I think, first I can find out the node with multiple parents... that cannot be right
I need to break off one of them

I can follow the parent link to find a root candidate and see if it connects the tree?
still very abstract but worthy a try?

need to go to a meeting soon
don't sweat too much

"""


class Solution:
    def findRedundantDirectedConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        roots = []
        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x, y):
            roots[find(x)] = find(y)

        def findRedundantConn():
            nonlocal roots
            roots = [i for i in range(n+1)]
            for p, c in edges:
                if find(c) == find(p):
                    return [p, c]
                union(c, p)
        
        def stillCycleAfterRemove(s,e):
            nonlocal roots
            roots = [i for i in range(n+1)]
            for p, c in edges:
                if(p,c) == (s,e):
                    continue
                if find(c) == find(p):
                    return True
                union(c, p)
            return False

        parentLinks = defaultdict(list)
        dblParentNode = -1

        for p,c in edges:
            parentLinks[c].append(p)
            if len(parentLinks[c]) == 2:
                dblParentNode = c
        
        if dblParentNode == -1:
            # a simple cycle detection? union find can help
            return findRedundantConn()
        else:
            # this node must become a single parent
            # just see taking which link off, the tree can be formed...
            # maybe it will work
            p1,p2 = list(parentLinks[dblParentNode])
            if stillCycleAfterRemove(p1, dblParentNode) or (not stillCycleAfterRemove(p2, dblParentNode)):
                return [p2,dblParentNode]
            return [p1, dblParentNode]
            
"""
Runtime: 108 ms, faster than 39.00% of Python3 online submissions for Redundant Connection II.
Memory Usage: 14.4 MB, less than 70.00% of Python3 online submissions for Redundant Connection II.

Runtime: 69 ms, faster than 66.33% of Python3 online submissions for Redundant Connection II.
Memory Usage: 14.4 MB, less than 70.00% of Python3 online submissions for Redundant Connection II.

not super effective
let me see the DFS route 

still similar idea
1. see if a node has two parents 
2. if not.. then find the first edge that forms a cycle
3. if yes.. break a edge and see if follows parent link can it return to itself to test if it is a cycle
"""


class Solution:
    def findRedundantDirectedConnection(self, edges: List[List[int]]) -> List[int]:
        parentLinks = defaultdict(list)
        dblParentNode = -1

        for p,c in edges:
            parentLinks[c].append(p)
            if len(parentLinks[c]) == 2:
                dblParentNode = c
        
        if dblParentNode == -1:
            ...

        else:
            # this node must have a single parent
            # just see taking which link off, the tree can be formed...
            # maybe it will work
            ...
        
        return None


if __name__ == '__main__':
    s = Solution()
    print(s.findRedundantDirectedConnection([[1, 2], [1, 3], [2, 3]]))
    print(s.findRedundantDirectedConnection([[2,1],[3,1],[4,2],[1,4]]))