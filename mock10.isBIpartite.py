from collections import deque
from typing import List


class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        blues = set()
        reds = set()
        colors = [blues, reds]
        color = 0

        visited = set()
        for start in range(len(graph)):
          if start in visited:
             continue
          q = deque()
          q.append((start,0))

          while q:
              node,color = q.popleft()
              
              if node in blues or node in reds:
                  continue
              visited.add(node)
              
              otherColor = color^1
              colors[color].add(node)
              for nei in graph[node]:
                  if nei in colors[color]:
                    return False
                  q.append((nei,otherColor))

        return True



                
            


