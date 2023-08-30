"""
so this is to find a path that is not leading to dest?


"""

from collections import defaultdict, deque
from functools import cache
from typing import List


class Solution:
    def leadsToDestination(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        neighbors = defaultdict(list)
        for n1,n2 in edges:
            neighbors[n1].append(n2)
        
        def toDest(node, path):
            if node in path:
                return False

            if (not neighbors[node]):
                return node == destination
                
            
            subPath = True
            for nei in neighbors[node]:
                if not toDest(nei, path.union({node})):
                    subPath = False
                    break
            return subPath
        
        return toDest(source, set())
    
    # how to apply cache???
    # 1. detect if there is loop? if not, then I don't need a path

    def leadsToDestination(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:

        roots = [i for i in range(n)]
        def find(x):
            if x!=roots[x]:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x,y):
            roots[x] = roots[find(y)]
        
        for n1,n2 in edges:
            if find(n1) == find(n2):
                return False
            union(n1,n2)

        neighbors = defaultdict(list)
        for n1,n2 in edges:
            neighbors[n1].append(n2)

        @cache
        def toDest(node):
            if (not neighbors[node]):
                return node == destination

            for nei in neighbors[node]:
                if not toDest(nei):
                    return False
            return True
        
        return toDest(source)
    
      # okay, this detect loop logic is not right
      # union find can only be applied to undirectional graph
    def leadsToDestination(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:


        neighbors = defaultdict(list)
        for n1,n2 in edges:
            neighbors[n1].append(n2)

        def hasCycle(node, path):
            if node in path:
                return True
            
            for nei in neighbors[node]:
                if hasCycle(nei, path.union({node})):
                    return True
            return False
        
        if hasCycle(source,set()):
            return False

        @cache
        def toDest(node):
            if (not neighbors[node]):
                return node == destination

            for nei in neighbors[node]:
                if not toDest(nei):
                    return False
            return True
        
        return toDest(source)
    

    def leadsToDestination(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:


        neighbors = defaultdict(list)
        for n1,n2 in edges:
            neighbors[n1].append(n2)

        visited = set()
        def hasCycle(node, path):
            if node in path:
                return True
            for nei in neighbors[node]:
                if nei not in visited and hasCycle(nei, path.union({node})):
                    return True
            visited.add(node)
            return False
        
        if hasCycle(source,set()):
            return False

        @cache
        def toDest(node):
            if (not neighbors[node]):
                return node == destination

            for nei in neighbors[node]:
                if not toDest(nei):
                    return False
            return True
        
        return toDest(source)
    
if __name__ == '__main__':
    s = Solution()
    # print(s.leadsToDestination(n = 2, edges = [[0,1],[1,1]], source = 0, destination = 1))
    # print(s.leadsToDestination(n = 4, edges = [[0,1],[0,2],[1,3],[2,3]], source = 0, destination = 3))
    print(s.leadsToDestination(n = 5, edges = [[0,1],[0,2],[0,3],[0,3],[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]], source = 0, destination = 4))
    