"""
https://leetcode.com/problems/connecting-cities-with-minimum-cost/

not quite sure the algorithm
maybe starting from any node... push the edges into the heap and pop 

this problem allows double edges.. but I can easily deal with it
I don't know if this is the right algorithm

let me try 
"""


from collections import defaultdict
import heapq
from typing import List


class Solution:
    def minimumCost(self, n: int, connections: List[List[int]]) -> int:
        
        connected = set()

        graph = defaultdict(set)

        for n1,n2,cost in connections:
            graph[n1].add((cost,n2))
            graph[n2].add((cost,n1))
        
        h = [] # cost, node
        heapq.heappush(h, (0,1)) 
        totalCost = 0
        while h and len(connected)<n:
            cost, node = heapq.heappop(h)
            totalCost += cost
            connected.add(node)        
            for w, v in graph[node]:
                if v in connected:
                    continue
                heapq.heappush(h, (w, v))
        

        if len(connected) == n:
            return totalCost 
        return -1

"""
26 / 63 test cases passed.


failed at 
4
[[1,2,1],[1,3,2],[3,4,4],[1,4,3]]


change the logic of maintaining cost.. 
51 / 63 test cases passed.

but still wrong

okay.. admit it I don't know the algorithm at all
another idea: start with shortest edges

and add them
for both ends in the connected graphs.. skip..
lastly see if I added n-1 edges...
"""


class Solution:
    def minimumCost(self, n: int, connections: List[List[int]]) -> int:
        connected = set()
        h = [] # weight, n1,n2
        for n1, n2, cost in connections:
            heapq.heappush(h, (cost, n1,n2))
        
        totalCost = 0
        edges = 0
        while h:
            cost,n1,n2 = heapq.heappop(h)
            if n1 in connected and n2 in connected:
                continue
            
            connected.add(n1)
            connected.add(n2)
            totalCost += cost
            edges += 1
        if edges == n-1:
            return totalCost
        return -1

"""
okay.. easily logical error and failed
7
[[2,1,87129],[3,1,14707],[4,2,34505],[5,1,71766],[6,5,2615],[7,2,37352]]

it needs a union find like
"""


class Solution:
    def minimumCost(self, n: int, connections: List[List[int]]) -> int:
        h = []  # weight, n1,n2
        for n1, n2, cost in connections:
            heapq.heappush(h, (cost, n1, n2))

        roots = [i for i in range(n+1)]
        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]
        
        def union(x,y):
            roots[find(x)] = roots[find(y)]

        totalCost = 0
        edges = 0
        while h:
            cost, n1, n2 = heapq.heappop(h)
            if find(n1) == find(n2):
                continue
            union(n1,n2)
            totalCost += cost
            edges += 1
            if edges == n-1:
                return totalCost
        return -1

"""
Runtime: 701 ms, faster than 56.25% of Python3 online submissions for Connecting Cities With Minimum Cost.
Memory Usage: 20.6 MB, less than 49.18% of Python3 online submissions for Connecting Cities With Minimum Cost.

okay so I actually figured out the Krushul algorithm myself
I can use sorting instead of heap to go thru the edges
but that is fine

as I remembered there is another algorithm for MST - PRIM
huh.. actually my first attempt is PRIM but where went wrong.. let me see

okay.. I didn't test the popped node for this
            cost, node = heapq.heappop(h)
            if node in connected:
                continue

but I did that in the adding heap part???

ah okay.. I see.. subtle error

A -> B <- C
|    |    | 
D -> E -> F 

B could be added into the queue by A, lets say w(A,B) = 2
and at some point C->B is smaller.. B is connected thru C

but B (added by A) is still in the heap and could become the smallest at some point..
so yeah.. the popped from queue could be in connected component already...

A -3->   B 
 \      /  \
  1    1    4
   \  /      \_
    C ---4---> D 

for example, such a graph.. 
when start from A.. B and C will be in queue like (1,C) (3,B)

C popped, will add (1,B) (3,B) (...)
B popped, will remain (3,B) ... 

so to minimize the computaion.. testing in both queue adding and popping is best for PRIM..


"""


class Solution:
    def minimumCost(self, n: int, connections: List[List[int]]) -> int:

        connected = set()

        graph = defaultdict(set)

        for n1, n2, cost in connections:
            graph[n1].add((cost, n2))
            graph[n2].add((cost, n1))

        h = []  # cost, node
        heapq.heappush(h, (0, 1))
        totalCost = 0
        while h and len(connected) < n:
            cost, node = heapq.heappop(h)
            if node in connected:
                continue
            totalCost += cost
            connected.add(node)
            for w, v in graph[node]:
                if v in connected:
                    continue
                heapq.heappush(h, (w, v))

        if len(connected) == n:
            return totalCost
        return -1

"""
Runtime: 695 ms, faster than 60.33% of Python3 online submissions for Connecting Cities With Minimum Cost.
Memory Usage: 22.1 MB, less than 6.52% of Python3 online submissions for Connecting Cities With Minimum Cost.


anyway.. subtle hard to remember but TIL...
"""

if __name__ == '__main__':
    s = Solution()
    print(s.minimumCost(4, [[1,2,1],[1,3,2],[3,4,4],[1,4,3]]))