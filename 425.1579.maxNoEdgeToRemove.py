""""
https://leetcode.com/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable/?envType=study-plan&id=graph-ii

seems pretty complicated - how to approache this problem?

first insight:
    if a type 3, overlaps other type, that other type can be removed 
    between a type 3 and other type, definitely removing other type???

    for alice, bob's only can be removed and vice versa


hmm... if I run union find for alice/bob respectively 
    what can be removed?
        1. redundant connections 
        2. I shall prioritize the type3.. (by sort)

        3. I need to tell if all the nodes are connected(that is a O(n) scan)

I cannot see fine details but let me simulate the first example 

Input: n = 4, edges = [[3,1,2],[3,2,3],[1,1,3],[1,2,4],[1,1,2],[2,3,4]]
sort: [[1,1,2],[1,1,3],[1,2,4],[2,3,4],[3,1,2],[3,2,3]]

doing Alice
0 1 2 3 4 
    3 3         <- 3,2,3
  3 3 3         <- 3,1,2
    4 4 4       <- 1,2,4 (2,3,4) is bob's type
                <- redundant 1,1,3
                <- redundant 1,1,2 
                2 redundant + 1 bob's

doing Bob
0 1 2 3 4 
    3 3         <- 3,2,3
  3 3 3         <- 3,1,2
      4 4       <- 2,3,4
                (all connected...) the other two can be removd for bob

if I save a set for alice, set(0,1,3) (index inside) can be removed
for bob, set(0,1) can be removed..
take the intersections 

see another example:
Input: n = 4, edges = [[3,1,2],[3,2,3],[1,1,4],[2,1,4]]
sort: [[1,1,4],[2,1,4],[3,1,2],[3,2,3]]

alice:
0 1 2 3 4
    3 3
  3 3 3 
  4 4 4 4
            can only remove set(2)

bob:
0 1 2 3 4
    3 3
  3 3 3
  4 4 4 4 
            can only remove set(1)

Input: n = 4, edges = [[3,2,3],[1,1,2],[2,3,4]]

alice:
0 1 2 3 4
    3 3
  3 3 3 4   <- two roots. not possible. can return -1 alreadys.

maybe it could work.. give a try


"""


from typing import List


class Solution:
    def maxNumEdgesToRemove(self, n: int, edges: List[List[int]]) -> int:
        edges.sort()
        roots = None

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x,y):
            roots[find(x)] = find(y)

        def removable(type):
            nonlocal roots
            roots = [i for i in range(n+1)]

            res = set()
            i = len(edges)-1
            while i>=0:
                t,s,e = edges[i]
                if (t!=3 and t!= type) or (find(s) == find(e)) :
                    res.add(i)
                else:
                    union(s,e)
                i-=1
            
            rootSet = set()
            for root in roots[1:]:
                r = find(root)
                if rootSet and r not in rootSet:
                    # at least two roots 
                    return None, -1
                rootSet.add(r)
            return res,0
        
        aliceSet, traverse = removable(1)
        if traverse == -1:
            return -1
        
        bobSet, traverse = removable(2)
        if traverse == -1:
            return -1
        
        return len(aliceSet.intersection(bobSet))


"""
Runtime: 7067 ms, faster than 7.06% of Python3 online submissions for Remove Max Number of Edges to Keep Graph Fully Traversable.
Memory Usage: 55.3 MB, less than 28.28% of Python3 online submissions for Remove Max Number of Edges to Keep Graph Fully Traversable.

wow.. at least it passes
think what can improve???

not much idea.. let me see some hints

kind like what I did
- Build the network instead of removing extra edges.
- Suppose you have the final graph (after removing extra edges). Consider the subgraph with only the edges that Alice can traverse. What structure does this subgraph have? How many edges are there?
- Use disjoint set union data structure for both Alice and Bob.
- Always use Type 3 edges first, and connect the still isolated ones using other edges.

checked Lee's code
maybe I can simplify the O(n) scan and replace sort with 3*O(N)?
"""


class Solution:
    def maxNumEdgesToRemove(self, n: int, edges: List[List[int]]) -> int:
        roots = None

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x, y):
            roots[find(x)] = find(y)

        def removable(type):
            nonlocal roots
            roots = [i for i in range(n+1)]

            res = set()
            myEdges = 0
            for i, (t,s,e) in enumerate(edges):
                if t==3:
                    if find(s) == find(e):
                        res.add(i)
                    else:
                        union(s, e)
                        myEdges += 1
            for i, (t, s, e) in enumerate(edges):
                if t == type:
                    if find(s) == find(e):
                        res.add(i)
                    else:
                        union(s, e)
                        myEdges += 1
                elif t!=3:
                    res.add(i)
            return res, myEdges==n-1

        aliceSet, traverse = removable(1)
        if not traverse:
            return -1

        bobSet, traverse = removable(2)
        if not traverse:
            return -1

        return len(aliceSet.intersection(bobSet))


"""
Runtime: 3571 ms, faster than 33.33% of Python3 online submissions for Remove Max Number of Edges to Keep Graph Fully Traversable.
Memory Usage: 55 MB, less than 30.30% of Python3 online submissions for Remove Max Number of Edges to Keep Graph Fully Traversable.

okay.. I see that nuance
                        
                elif t!=3:
                    res.add(i)

yeah.. this can be done in one go
"""


class Solution:
    def maxNumEdgesToRemove(self, n: int, edges: List[List[int]]) -> int:
        roots = [i for i in range(n+1)]
        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x, y):
            roots[find(x)] = find(y)

        res = set()
        edgesA = edgesB = 0

        # alice and bob
        for i, (t, s, e) in enumerate(edges):
            if t == 3:
                if find(s) == find(e):
                    res.add(i)
                else:
                    union(s, e)
                    edgesA += 1
                    edgesB += 1
        # make a copy
        rootsB = roots[:]
        # alice
        # if it is redundant for alice and alice's only edge
        # it can be added to res.. because bob won't be able to walk this anyway
        for i, (t, s, e) in enumerate(edges):
            if t == 1:
                if find(s) == find(e):
                    res.add(i)
                else:
                    union(s, e)
                    edgesA += 1

        # bob
        roots = rootsB
        for i, (t, s, e) in enumerate(edges):
            if t == 2:
                if find(s) == find(e):
                    res.add(i)
                else:
                    union(s, e)
                    edgesB += 1

        return len(res) if edgesA == n-1 and edgesB == n-1 else -1


"""
wait.. somewhere is wrong
the roots[] are fully connected after processing alice..  (example 1)

how to do bob???

        # only Bob
        root = root0

ah.. it saved a copy after type3 and then use that one

Runtime: 2591 ms, faster than 46.97% of Python3 online submissions for Remove Max Number of Edges to Keep Graph Fully Traversable.
Memory Usage: 55.7 MB, less than 27.78% of Python3 online submissions for Remove Max Number of Edges to Keep Graph Fully Traversable.


okay..
"""

if __name__ == '__main__':
    s = Solution()
    print(s.maxNumEdgesToRemove(n = 4, edges = [[3,1,2],[3,2,3],[1,1,3],[1,2,4],[1,1,2],[2,3,4]]))