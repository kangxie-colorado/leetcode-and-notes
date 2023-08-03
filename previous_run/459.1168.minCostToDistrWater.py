"""
https://leetcode.com/problems/optimize-water-distribution-in-a-village/

a bit hard to think but very good problem I can see

for each house, 
    - either build a well 
    - connect from another well 
        not necessarily all the house can be connected
        then it only has the choice to build well..

let me see
for each connected component 
    - select the min cost to build well
    - compute the MST, that starting cost+MST will be total cost??????
        just think this for a while..
        ..
for each house
    - build a well vs connect to other component
        if the cost of building<min(edge weight)
            build?

a little spark comes up
    1. build the MST for all connected houses...
        MST(h1,h2,h3) -> 10
        lets see the forms (these are birectional)
            h1 <-5-> h2 <-5-> h3
            and wells cost for h1,h2,h3 are same 6 (if <5, then it is better to build)
            where to put it?
            use leetcode to help - 6+10 = 16

            let me see if h2=6,h1=h3=7 (rotating the 6) -- same 16
            yeah.. the problem asks for pipes' cost + well cost
            I was kind of thinking the water flowing cost... (invalid here)

        so looks like, if there is MST for connected component 
        I can choose the min cost to build it.. even connecting is cheaper than build

            in above case, if h1=h2=h3=4, then it is cheaper just to build 
            how to decide this?????
            just see for one house
                if build cost is costBuild
                connect cost is min(cost of its edges.. we can simply discard duplicate edges with higher cost, right?)

                if connect cost is  > costBuild:
                    for its own good.. build
                    but for other nodes?

                    hmm.. if it is the lowest build cost, then need to make a decision
                        otherwise, I should just disconnect it, right? maybe this is true

                    if it is indeed the min cost.. 
                        and its connect cost > build cost..
                        we need to see taking it out the overall cost, getting bigger or smaller???
                        but how to easily calculate that??
                            thoughts train continue to go down
                                thinking for each node, I can use (buildCost, connCost) to track its various cost
                                <- back
                    
                    hmm... still very complicated
            
            I guess there needs to be some greedy property somewhere?
                                       
============= 
just some random thoughts here

if I start building up the MST.. 
I can sort the edges by cost..
then union the lowest edges... (using find to skip duplicate edges with higher cost)
    ^^^ these steps are not hard

then I can keep a min build cost for that MST
if a new node comes up.. 
    if its build cost is bigger than minBuild.. 
        its connect cost is smaller than build cost.. then union it
        otherwise, union itself 
    if its build cost is even smaller than minBuild
        its connect cost is smaller than build cost.. then union it
        otherwise??? 
            check connect cost vs current minBuild???
                maybe.. this is basically replace a minBuild with a connectCost
                so connCost<=minBuild.. connect
                else: union itself... 

getting somewhere??
let me run an example


Input: n = 3, wells = [1,2,2], pipes = [[1,2,1],[2,3,1]]
edges are sorted naturally
->[1,2,1]
    connCost 1, minBuild 1 (1vs2)
->[2,3,1]
    3 is not in the component 
    connCost is 1. build cost is 2 -> connect
    connCost is 2, minBuild 1
    => 3

the case is way too simple  try another one
                        
Input: n = 2, wells = [1,1], pipes = [[1,2,1],[1,2,2]]
edges are sorted
-> [1,2,1]
    connCost 1, minBuild 1
-> [1,2,2]
    dup edges.. skip

    all houses are covered.. 2

still not revealing anything
===

let me see
n=5, wells=[5,10,10,10,10], pipes = [[[2,3,1],[2,4,1],[2,5,1],[1,2,6]]
(the sorting also puts pipes start with same house together, so union to first house)
-> [2,3,1]
    connCost 1, minBuild 10

-> [2,4,1]
    2 is in a component
    4 is new.. with buildCost 10

    connCost 2, vs buildCost 10->connect

-> [2,5,1]
    -> connect
    connCost 3, minBuild 10

-> [1,2,6]
    1 is new: connCost 6, build cost 5
        what to do?
    first.. buildCost < minBuild
        also connectCost < minBuild -> connect 
            connCost 9, minBuild 5 --> 14

twist it
n=5, wells=[5,10,6,10,10], pipes = [[[2,3,1],[2,4,1],[2,5,1],[1,2,6]]

after first 3 edages..
    connCost  3, minBuild 6

-> [1,2,6]
    1 is new..
    connCost 6 > buidCost 5 
    connCost == minBuild
        if connect, we replace minBuild cost with a connectCost an dupdate minBuild
            connectCost 9, minBuild 5 => 14
        if we don't, it is a single 5 + 9 still 14 

twist it
n=5, wells=[5,10,5,10,10], pipes = [[[2,3,1],[2,4,1],[2,5,1],[1,2,6]]

after first 3 edages..
    connCost  3, minBuild 5

-> [1,2,6]
    1 is new..
    connCost 6 > buidCost 5 
    connCost > minBuild
        if we replace, we replace 5 with 6 getting bigger, bad deal
        so leave it alone and total being 13 (5+8)

twist it
n=5, wells=[5,10,8,10,10], pipes = [[[2,3,1],[2,4,1],[2,5,1],[1,2,6]]

    this need to connect, 14

twist it
n=5, wells=[10,10,6,10,10], pipes = [[[2,3,1],[2,4,1],[2,5,1],[1,2,6]]

after first 3 edages..
    connCost  3, minBuild 6

-> [1,2,6]
    1 is new..
    connCost 6 < buidCost 10, need to connect 
    connCost == minBuild (doesn't matter)

    9+6 = 15

for above cases.. it checks out
but this is only one component.. for different component.. possibly we can do the same?
this could generalize.. even for two houses.. 

one house alone, we have to build.. and conncost is 0
then another house comes.. if they connect, we can either 
    - connect, if 
        connect cost is smaller than its build cost
        its build cost is smaller than previouse and connect cost is smaller than previous build cost (replace)
    - build, if
        connect cost is bigger than its build cost

at the end, for non-connected house, we just calculate its build cost
for connected houses.. 
    we need to maintain its minBuild??
    we always union to the house with smaller buildCost I guess could do that..

some thinking are possibly on the right direction.. let me give a try

rules recap
    if its build cost is bigger than minBuild.. 
        its connect cost is smaller than build cost.. then union it
        otherwise, union itself 
    if its build cost is even smaller than minBuild
        its connect cost is smaller than build cost.. then union it
        otherwise??? 
            check connect cost vs current minBuild???
                maybe.. this is basically replace a minBuild with a connectCost
                so connCost<=minBuild.. connect
                else: union itself... 

    this will generalize to 
                if h2BuildCost > connCost or connCost < h1BuildCost:    
                    union(h1, h2)
        basically if connCost is smaller than any of minBuildCost for two components
        union two components.. 
        it feels right but I don't know

    meantime looks like I need to keep MST cost in the roots? nah.. bad idea
    maybe a separate list

"""


from collections import defaultdict
import heapq
from typing import List


class Solution:
    def minCostToSupplyWater(self, n: int, wells: List[int], pipes: List[List[int]]) -> int:

        roots = [i for i in range(n+1)] # houses are from 1 to n
        mstConnCostAtRoots = [0]*(n+1) # padding to make 1-base easier
        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]
        
        def union(x,y, connCost):
            r1 = find(roots[x])
            r2 = find(roots[y])

            if wells[r1-1] < wells[r2-1]:
                roots[r2] = roots[r1]
            else:
                roots[r1] = roots[r2]

            # adding 
            totalMstConnCost = mstConnCostAtRoots[r2] + \
                mstConnCostAtRoots[r1] + connCost
            mstConnCostAtRoots[r1] = mstConnCostAtRoots[r2] = totalMstConnCost

        pipes.sort(key=lambda x: x[2])

        for h1,h2,connCost in pipes:
            # treat which one as new??? just treat h2.. because the sort put h1 togother
            # maybe there is some logical problem.. 
            # and h2 could already be in another group
            # but again.. this is build cost vs conn cost replacement
            if find(h1) != find(h2):
                h2BuildCost = wells[find(h2)-1] 
                h1BuildCost = wells[find(h1)-1] 

                # this seems symmetric and maybe correct
                if h2BuildCost > connCost or connCost < h1BuildCost:    
                    union(h1, h2, connCost)
        
        rootGrp = defaultdict(set)
        
        for h in range(1,n+1):
            root = find(h)
            rootGrp[root].add(h)
        
        totalCost = 0
        for root in rootGrp:
            totalCost += mstConnCostAtRoots[root] + wells[root-1]
        
        return totalCost

"""
Runtime: 493 ms, faster than 83.25% of Python3 online submissions for Optimize Water Distribution in a Village.
Memory Usage: 20.5 MB, less than 70.94% of Python3 online submissions for Optimize Water Distribution in a Village.

what a genius idea
https://leetcode.com/problems/optimize-water-distribution-in-a-village/discuss/365853/C%2B%2BPythonJava-Hidden-Well-in-House-0

just think there is a house 0(or a river)
we add the river(house 0) to the loop and make every house directly/indirectly connected to the river
thus the wells cost also becomes an edge [0,i,wells[i]]..

this way.. it becomes a pure MST problem!!!
"""


class Solution:
    def minCostToSupplyWater(self, n: int, wells: List[int], pipes: List[List[int]]) -> int:
        for i,cost in enumerate(wells):
            pipes.append([0,i+1,cost])
        
        roots = [i for i in range(n+1)]
        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]
        
        def union(x,y):
            roots[find(x)] = roots[find(y)]

        pipes.sort(key=lambda x:x[2])
        totalCost = 0
        for h1,h2,cost in pipes:
            if find(h1) != find(h2):
                union(h1,h2)
                totalCost += cost 
        return totalCost

""""
Runtime: 495 ms, faster than 81.53% of Python3 online submissions for Optimize Water Distribution in a Village.
Memory Usage: 20.7 MB, less than 63.55% of Python3 online submissions for Optimize Water Distribution in a Village.

let me do that PRIM algorithm
I still treat the water source as house 0.. it has a cost to each house of wells[i-1]

and I start with that house 0.. 
PRIM is dealing with closest vertext.. using a heap.. and it also relax the cost to each other vertex..
how to get to the weight??? delta?

I kind of unsure now.. let me try anyway
"""


class Solution:
    def minCostToSupplyWater(self, n: int, wells: List[int], pipes: List[List[int]]) -> int:
        graph = defaultdict(set)
        for h1,h2,cost in pipes:
            graph[h1].add((h2,cost))
            graph[h2].add((h1,cost))
        
        h = []
        for i,cost in enumerate(wells):
            heapq.heappush(h, (cost, i+1))
        
        totalCost = 0
        connected = set()
        while h and len(connected) < n:
            cost,house = heapq.heappop(h)
            if house in connected:
                continue
            totalCost += cost
            connected.add(house)

            for nei,neiCost in graph[house]:
                if nei in connected:
                    continue
                heapq.heappush(h, (neiCost, nei))
        
        return totalCost

"""
Runtime: 522 ms, faster than 62.07% of Python3 online submissions for Optimize Water Distribution in a Village.
Memory Usage: 22.4 MB, less than 12.56% of Python3 online submissions for Optimize Water Distribution in a Village.

"""



        
if __name__ == '__main__':
    s = Solution()
    print(s.minCostToSupplyWater(n=3, wells=[
          1, 2, 2], pipes=[[1, 2, 1], [2, 3, 1]]))
                