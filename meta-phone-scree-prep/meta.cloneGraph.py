"""
did this before but still not easy
"""

"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""
from collections import defaultdict, deque


class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        newNode = Node(node.val, node.neighbors)

        q = deque()
        q.append(newNode)
        visited = set()
        cloned = defaultdict(Node)

        while q:
            n = q.popleft()
            if n in visited:
                continue
            
            visited.add(n)
            newNeighbors = []
            for nei in n.neighbors:
                newNei = Node(nei.val, nei.neighbors)
                if nei.val in cloned:
                    newNei = cloned[nei.val]
                
                newNeighbors.append(newNei)
                q.append(newNei)
            
            n.neighbors = newNeighbors
            cloned[n.val] = n
        
        return newNode

"""
okay.. this solution does not work
let me think 

lets clone every one of them
then re-connect
"""

class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        if not node:
            return None
        q = deque()
        q.append(node)
        visited = set()
        cloned = {}

        while q:
            n = q.popleft()
            if n in visited:
                continue
            visited.add(n)

            newNode = Node(n.val, n.neighbors)
            cloned[n] = newNode

            for nei in n.neighbors:
                q.append(nei)
        
        for old,new in cloned.items():
            newNeighbors = []
            for nei in old.neighbors:
                newNeighbors.append(cloned[nei])
            new.neighbors = newNeighbors
          
        return cloned[node]


        
      

if __name__ == '__main__':
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n1.neighbors = [n2]
    n2.neighbors = [n1,n3]
    n3.neighbors = [n2]

    Solution().cloneGraph(n1)
    