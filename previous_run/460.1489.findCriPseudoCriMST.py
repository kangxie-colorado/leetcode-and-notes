"""
https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/

Jeesus Crist!
where to start?

critical: seems like the choice I must have, by sorting 
pseudo-critical: seems like the equivilent choices when adding the edges to MST?


1 <= weighti <= 1000
not very big indeed... can I go thru one by one?

I put it in a bucket the same weight 
and when adding edges... if the edge connects
    - two components which were not connected yet.. then critical
        nah.. think example 2
    - two components ? 


hmm.. 
so pick up a bucket, edges with equal weights...
    - connect them.. if they don't create a cycle then they are critical
    - if they create a cycle... then what?
        then what forms the cycle are pseudo-critical 
            then I need to know which edges are in the cycle?
            cause there are still critical in this case : critical + pseudo both
            e.g. 1 --- 2 --- 4
                       |     |
                       |     |
                       3-----|
                1-to-2 is critical
                2-3-4 only needs any too
            how to model this?                    

like?
    - just try adding all.. if no cycle.. then good
    - if there is a cycle.. 
        then remove one edge.. 
            cycle stands.. it is critical
            cycle disappears.. it is pseudo
            but this is going to be repeating a lot

anyway.. let me try
"""


from typing import List


class Solution:
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:

        # 1 <= weighti <= 1000, I create 1001 buckets to store the edges per weight 
        edgesByWeigth = [[] for _ in range(1001)]
        for idx, (n1,n2,w) in edges:
            edgesByWeigth[w].append((n1,n2, idx))
        
        roots = [i for i in range(n)]
        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]
        
        def union(x,y):
            roots[find(x)] = roots[find(y)]

        def f(roots, edges):
            ...

        # res = []
        for w,edges in edgesByWeigth:
            if not edges:
                continue

            # at currently unprocessed min-weight(w)
            # edges are the cheapest 
            cycle = False
            for n1,n2, idx in edges:
                if find(n1) != find(n2):
                    union(n1,n2)
                else:
                    # there are cycles... shit...
                    cycle =  True
                    break
            
            if not cycle:
                # res.extend([idx for _,_,idx in edges])
                ...
            else:
                # hmm.. wait.. 
                # it asks only to return the indices. 
                # I don't have to distiguish 
                # so the truly unadded edges are truly redudant
                # i.e. their nodes are connected by lower weights... 
                # look at example 1.. kind of like this
                # I only need to pre-test if the n1.n2 are pre-connected
                # and union them later... start a new one to 
                # pause this here
                ...

        return None


class Solution:
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:

        # 1 <= weighti <= 1000, I create 1001 buckets to store the edges per weight
        edgesByWeigth = [set() for _ in range(1001)]
        for idx, (n1, n2, w) in enumerate(edges):
            edgesByWeigth[w].add((n1, n2, idx))

        roots = [i for i in range(n)]

        def find(roots, x):
            if roots[x] != x:
                roots[x] = find(roots, roots[x])
            return roots[x]

        def union(roots, x, y):
            roots[find(roots, x)] = roots[find(roots, y)]

        def hasCycle(roots, pairs, skipIdx):
            # I use this to check after removing an edge 
            # there is no cycle anymore
            # if no more cycle.. then it is pseudo
            # otherwise, there is still cycle... then it is critical
            # actually I eliminated the totally redundant links already
            # I only need to find out the critical or pseudo ones
            # the other type can be simply get by doing substraction...
            # but even with this.. there is no good ways to tell critical from pseudo...
            # I'll detect hasCycle... 
            for n1,n2,idx in pairs:
                if idx == skipIdx:
                    continue
                if find(roots, n1) == find(roots, n2):
                    return True
                union(roots, n1,n2)
            return False

        criticals = []
        psedudos = []
        for w, pairs in enumerate(edgesByWeigth):
            if not pairs:
                continue
            
            redundant = set()
            for n1, n2, idx in pairs:
                if find(roots, n1) == find(roots, n2):
                    redundant.add((n1, n2, idx))
            
            pairs = pairs.difference(redundant)
            unionsBackup = list(roots) # saved before union to detect cycle
            cycle = False 
            for n1, n2, idx in pairs:
                if find(roots, n1) != find(roots, n2):
                    union(roots, n1,n2)
                else:
                    cycle = True
                    # no need to break.. let it union all
                    # anyway the union needs to happen
                                
            if not cycle:
                criticals.extend(
                    [idx for _, _, idx in pairs if idx not in redundant])
            else:
                # need to test if an edge is critical
                for n1, n2, idx in pairs:
                    if hasCycle(list(unionsBackup), pairs, idx):
                        criticals.append(idx)
                    else:
                        psedudos.append(idx)
                
            # ah.. not that simlpe..
            # critical and pseudo must be output in two parts.. 
            # feel like I need to go back to ealier thoughts
            # think this need to happen before union everything together
            # before this for loop.. comments are left here but cursor moves back
        
        return [criticals, psedudos]
    

"""
better than I thought 49/66 passed
failed here
Input:
4
[[0,1,1],[0,3,1],[0,2,1],[1,2,1],[1,3,1],[2,3,1]]
Output: [[5,1,0,2,3,4],[]]
Expected: [[],[0,1,2,3,4,5]]

interesting..why I thought them all to be critical???
ah.. removing any edge there is still cycle.. and I added it to criticl.. 
probably that condition is not necessarily true

removing an edge.. there is still cycel.. it can be critical or pseudo..
removing an edge.. cycle disappears.. then it must be presudo...

so that f() function is wrong.. how to fix that?
actually can be this way
    - adding all the edges but the test-one to unoin and avoid cycle.. 
    - now see if this test-edge is redundant.. 
        if yes, pseudo for sure
        if not, its critical

copy/cleanup/continue
"""


class Solution:
    def findCriticalAndPseudoCriticalEdges(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        # 1 <= weighti <= 1000, I create 1001 buckets to store the edges per weight
        edgesByWeigth = [set() for _ in range(1001)]
        for idx, (n1, n2, w) in enumerate(edges):
            edgesByWeigth[w].add((n1, n2, idx))

        roots = [i for i in range(n)]

        def find(roots, x):
            if roots[x] != x:
                roots[x] = find(roots, roots[x])
            return roots[x]

        def union(roots, x, y):
            roots[find(roots, x)] = roots[find(roots, y)]

        def pseudoLink(roots, pairs, skipIdx):
            # adding this edge and a cyle.. then it has to be pseudo
            # doing this I add all other edges but avoid cycle
            pN1=pN2=-1
            for n1, n2, idx in pairs:
                if idx == skipIdx:
                    pN1,pN2 = n1,n2
                    continue
                if find(roots, n1) != find(roots, n2):    
                    union(roots, n1, n2)
            if find(roots, pN1) == find(roots, pN2):
                return True
            return False

        criticals = []
        psedudos = []
        for w, pairs in enumerate(edgesByWeigth):
            if not pairs:
                continue

            redundant = set()
            for n1, n2, idx in pairs:
                if find(roots, n1) == find(roots, n2):
                    redundant.add((n1, n2, idx))

            pairs = pairs.difference(redundant)
            unionsBackup = list(roots)  # saved before union to detect cycle
            cycle = False
            for n1, n2, idx in pairs:
                if find(roots, n1) != find(roots, n2):
                    union(roots, n1, n2)
                else:
                    cycle = True

            if not cycle:
                criticals.extend(
                    [idx for _, _, idx in pairs if idx not in redundant])
            else:
                # need to test if an edge is critical
                for n1, n2, idx in pairs:
                    if pseudoLink(list(unionsBackup), pairs, idx):
                        psedudos.append(idx)
                    else:
                        criticals.append(idx)

        return [criticals, psedudos]


"""
okay.. still error

6
[[0,1,2],[0,2,5],[2,3,5],[1,4,4],[2,5,5],[4,5,2]]
Output: [[5,0,3],[1,4]]
Expected: [[0,2,3,5],[1,4]]

okay I forgot to update the critical part

omg..

Runtime: 85 ms, faster than 97.48% of Python3 online submissions for Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree.
Memory Usage: 14.3 MB, less than 12.61% of Python3 online submissions for Find Critical and Pseudo-Critical Edges in Minimum Spanning Tree.

https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/discuss/697761/C%2B%2B-Solution-enumerating-edges-with-explanation
checked other's code.. I think mine is better actually

but more complex logically maybe.. anyway.. revisit this later
"""

if __name__ == '__main__':
    s = Solution()
    print(s.findCriticalAndPseudoCriticalEdges(6,[[0,1,2],[0,2,5],[2,3,5],[1,4,4],[2,5,5],[4,5,2]]))
    print(s.findCriticalAndPseudoCriticalEdges(4,[[0,1,1],[0,3,1],[0,2,1],[1,2,1],[1,3,1],[2,3,1]] ))
    print(s.findCriticalAndPseudoCriticalEdges(n = 4, edges = [[0,1,1],[1,2,1],[2,3,1],[0,3,1]]))
    print(s.findCriticalAndPseudoCriticalEdges(n = 5, edges = [[0,1,1],[1,2,1],[2,3,2],[0,3,2],[0,4,3],[3,4,3],[1,4,6]]))