"""
thinking the water source is a big well in house-0

build cost is the pipe cost from each house to house-0
such that 
Input: n = 3, wells = [1,2,2], pipes = [[1,2,1],[2,3,1]]
becomes a problem that can be described as 

pipes = [[0,1,1],[0,2,2],[0,3,2],[1,2,1],[2,3,1]]
the problem is now get the MST out of this graph..

but how to get MST????
maybe it is find the min cost edge, using heap..

once all the nodes are connected, it is done?

"""

from collections import defaultdict
import heapq
from typing import List


class Solution:
    def minCostToSupplyWater(self, n: int, wells: List[int], pipes: List[List[int]]) -> int:
        graph = []
        for well,cost in wells:
            graph.append([0,well+1,cost])
        graph.extend(pipes)

        # find mst in this graph
        h = []
        for n1,n2,cost in graph:
            heapq.heappush(h, (cost, n1,n2))
        
        connected = set()
        totalCost = 0
        while len(connected) < n+1 and h:
            cost,n1,n2 = heapq.heappop(h)
            if n1 in connected and n2 in connected:
                continue
            totalCost += cost 
            connected.add(n1)
            connected.add(n2)
        
        return totalCost

"""
this algorithm is not like this.
it needs to be dynamically discovered for next node to add

I should start from node-0
pick the smallest? 
"""

class Solution:
    def minCostToSupplyWater(self, n: int, wells: List[int], pipes: List[List[int]]) -> int:
        graph = []
        h = []
        for well,cost in enumerate(wells):
            graph.append([0,well+1,cost])
            heapq.heappush(h, (cost, well+1))
        graph.extend(pipes)
        # build adjacent set
        adjNeighbors = defaultdict(list)
        for _,n1,n2 in graph:
            adjNeighbors[n1].append((n2,cost))
            adjNeighbors[n2].append((n1,cost))

        # find mst in this graph
        connected = set()
        connected.add(0)
        while h:
            cost,node = heapq.heappop(h)
            if node in connected:
                continue
            connected.add(node)
            if len(connected)==(n+1):
                return cost 
            for nei,pipe in adjNeighbors[node]:
                heapq.heappush(h, (cost+pipe, nei))


"""
okay.. this algorithm is still run, it is used to get ..
hmm.. it is nonsense of my code

I have to look up what is MST
so it indeed relies on union-find, sort the edges by cost, pick smallest
if no cycle, continue to include
else skip it

I should work on my first try
"""

class Solution:
    def minCostToSupplyWater(self, n: int, wells: List[int], pipes: List[List[int]]) -> int:
        graph = []
        for well,cost in enumerate(wells):
            graph.append([0,well+1,cost])
        graph.extend(pipes)
        graph.sort(key=lambda x: x[2])

        roots = [i for i in range(n+1)]
        def find(x):
            if x!=roots[x]:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x,y):
            roots[find(x) ] = roots[find(y)]

        totalCost = 0
        for n1,n2,cost in graph:
            if find(n1) != find(n2):
                union(n1,n2)
                totalCost += cost 
        return totalCost


class Solution:
    def minCostToSupplyWater(self, n: int, wells: List[int], pipes: List[List[int]]) -> int:
        graph = []
        h = []
        for well,cost in enumerate(wells):
            graph.append([0,well+1,cost])
            heapq.heappush(h, (cost, well+1))
        graph.extend(pipes)
        # build adjacent set
        adjNeighbors = defaultdict(list)
        for n1,n2,cost in graph:
            adjNeighbors[n1].append((n2,cost))
            adjNeighbors[n2].append((n1,cost))

        # find mst in this graph
        connected = set()
        connected.add(0)
        totalCost = 0
        while h:
            cost,node = heapq.heappop(h)
            if node in connected:
                continue
            connected.add(node)
            totalCost += cost
            if len(connected)==(n+1):
                return totalCost
            for nei,pipe in adjNeighbors[node]:
                if nei in connected:
                    continue
                heapq.heappush(h, (pipe, nei))
        
if __name__ == '__main__':
    s = Solution()
    print(s.minCostToSupplyWater(n = 3, wells = [1,2,2], pipes = [[1,2,1],[2,3,1]]))
      
            

