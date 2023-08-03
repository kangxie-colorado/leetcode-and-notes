"""
https://leetcode.com/problems/min-cost-to-connect-all-points/

this is exactly the MST
but how to get the edges? just O(n**2)?

maybe I can sort?? no use
"""


import heapq
from typing import List


class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        connected = set()

        totalCost = 0
        h = [(0, *points[0])] # cost, (x,y)
        while len(connected) < n:

            cost,x,y = heapq.heappop(h)
            if (x,y) in connected:
                continue
            totalCost+=cost
            connected.add((x,y))

            for nx,ny in points:
                if (nx,ny) in connected:
                    # this takes care of nx,ny == x,y case
                    continue
                    
                heapq.heappush(h, ( abs(nx-x)+abs(ny-y),  nx,ny))
        return totalCost


"""
Runtime: 3141 ms, faster than 52.09% of Python3 online submissions for Min Cost to Connect All Points.
Memory Usage: 67.6 MB, less than 87.23% of Python3 online submissions for Min Cost to Connect All Points.

do the krushul too

this is n**2 edges vs N vertex.. so DENSE.. PRIM is really better
but whatever
"""


class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)

        edges = []
        for i in range(n):
            for j in range(i+1,n):
                (x1,y1),(x2,y2) = points[i], points[j]
                edges.append((abs(x1-x2)+abs(y1-y2), i, j))
        
        edges.sort()
        
        roots = [i for i in range(n)]
        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]
        
        def union(x, y):
            roots[find(x)] = roots[find(y)]
        
        connectEdges = 0
        totalCost = 0
        for l,p1,p2 in edges:
            if find(p1) != find(p2):
                union(p1,p2)
                totalCost += l
                connectEdges += 1
                if connectEdges == n-1:
                    break
        
        return totalCost


"""
Runtime: 2448 ms, faster than 64.16% of Python3 online submissions for Min Cost to Connect All Points.
Memory Usage: 81.5 MB, less than 73.55% of Python3 online submissions for Min Cost to Connect All Points.

okay..

actually there is one and only one connected component
so there is no need for unoin find? nah.. still need that
"""