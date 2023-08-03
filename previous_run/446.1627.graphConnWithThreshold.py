"""
https://leetcode.com/problems/graph-connectivity-with-threshold/?envType=study-plan&id=graph-ii

interesting ...
union-find of course, when two integers share the factor>threshold, they union

but the things is if I pre-union, there is 10**4 cities
it will be like O(n**2) can it pass

but anyway... maybe there are optimization to that
I want to get a basic working solution even with TLE first

"""



import math
from typing import List


class Solution:
    def areConnected(self, n: int, threshold: int, queries: List[List[int]]) -> List[bool]:
        if threshold == 0:
            return [True] * len(queries)

        roots = [i for i in range(n+1)]

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]
        
        def union(x,y):
            roots[find(x)] = roots[find(y)]
        
        for i in range(1,n+1):
            for j in range(i+1,n+1):
                if math.gcd(i,j) > threshold:
                    union(i,j)
        
        res = [False] * len(queries)
        for i, q in enumerate(queries):
            c1,c2 = q
            if find(c1) == find(c2):
                res[i] = True
        
        return res

"""
65 / 67 test cases passed.
TLE... 
not too bad...

to optimize:
    I think reducing the pairs to union might be that place
    I could start from first number's smallest factor that is biggest than threshold?
    then adding all the rest numbers 

hints:
    How to build the graph of the cities?
    Connect city i with all its multiples 2*i, 3*i, ...
    Answer the queries using union-find data structure.

okay.. so lets just start with threshold+1
"""


class Solution:
    def areConnected(self, n: int, threshold: int, queries: List[List[int]]) -> List[bool]:
        if threshold == 0:
            return [True] * len(queries)

        roots = [i for i in range(n+1)]

        def find(x):
            if roots[x] != x:
                roots[x] = find(roots[x])
            return roots[x]

        def union(x, y):
            roots[find(x)] = roots[find(y)]

        # think this is the place to optimize
        # 
        f = threshold + 1
        # while f <= n:
        while 2*f <= n:
            n1 = f
            i = 2
            while i*f <= n:
                union(n1, i*f)
                i+=1
            f+=1

        res = [False] * len(queries)
        for i, q in enumerate(queries):
            c1, c2 = q
            if find(c1) == find(c2):
                res[i] = True

        return res

"""
Runtime: 1427 ms, faster than 35.88% of Python3 online submissions for Graph Connectivity With Threshold.
Memory Usage: 49.4 MB, less than 27.48% of Python3 online submissions for Graph Connectivity With Threshold.

Runtime: 835 ms, faster than 95.42% of Python3 online submissions for Graph Connectivity With Threshold.
Memory Usage: 49.4 MB, less than 27.48% of Python3 online submissions for Graph Connectivity With Threshold.
"""