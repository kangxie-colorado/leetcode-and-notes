"""
https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/?envType=study-plan&id=graph-ii

floyd-warshall and search under threshold.. 
"""


from typing import List


class Solution:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:

        dist = [[float('inf')]*n for _ in range(n)]

        for i in range(n):
            dist[i][i] = 0

        for i, j, d in edges:
            dist[i][j] = dist[j][i] = d

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])        
        minReach = float('inf')
        res = -1
        for i, r in enumerate(dist):
            reach = sum([k <= distanceThreshold for k in r ])
            if reach <= minReach:
                minReach = reach
                res = i
        return res

if __name__ == '__main__':
    s = Solution()
    print(s.findTheCity( n = 4, edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], distanceThreshold = 4))
