"""
https://leetcode.com/problems/parallel-courses/?envType=study-plan&id=graph-ii

seems like the layer of bfsQ can solve 
"""


from collections import defaultdict, deque
from typing import List


class Solution:
    def minimumSemesters(self, n: int, relations: List[List[int]]) -> int:
        graph = defaultdict(set)
        incomingLinks = [0] * (n+1)
        for pre,course in relations:
            graph[pre].add(course)
            incomingLinks[course] += 1
        
        bfsQ = deque()
        for c in range(1,n+1):
            if incomingLinks[c] == 0:
                bfsQ.append(c)
            
        res = 0
        taken = 0
        while bfsQ:
            l = len(bfsQ)
            while l:
                c = bfsQ.popleft() 
                taken += 1

                for dep in graph[c]:
                    incomingLinks[dep] -= 1
                    if incomingLinks[dep] == 0:
                        bfsQ.append(dep)
                l-=1
            res += 1
        return res if taken == n else -1


"""
Runtime: 260 ms, faster than 96.09% of Python3 online submissions for Parallel Courses.
Memory Usage: 16.8 MB, less than 73.45% of Python3 online submissions for Parallel Courses.

I am thinking how to solve this in DFS?
having no idea.. then checked the hints.. pretty cool

- Try to think of it as a graph problem. It will be impossible to study all the courses if the graph had a cycle.
- The graph is a directed acyclic graph (DAG). The answer is the longes path in this DAG.
- You can use DP to find the longest path in the DAG.

so longest path.. 
let me try
"""


class Solution:
    def minimumSemesters(self, n: int, relations: List[List[int]]) -> int:
        depth = [0] * (n+1)

        graph = defaultdict(set)
        for pre, course in relations:
            graph[pre].add(course)
        
        def dfs(c):
            if depth[c] > 0:
                # processed
                return depth[c]
            
            if depth[c] == n+1:
                # in the same path: cycle
                # this can be consolidated into above if.. but just leave here for self-explanation
                return n+1
            
            # set to path (using n+1 to represent that)
            depth[c] = n+1
            subDepth = 0
            for dep in graph[c]:
                subDepth = max(subDepth, dfs(dep))
                if subDepth == n+1:
                    return n+1
                
            depth[c] = 1 + subDepth
            return depth[c]
        
        res = 0
        for c in range(n):
            res = max(res, dfs(c)) 
        
        return res if res!=n+1 else -1

"""
Runtime: 813 ms, faster than 8.82% of Python3 online submissions for Parallel Courses.
Memory Usage: 19.4 MB, less than 5.09% of Python3 online submissions for Parallel Courses.


aha.. surprised to see it pass 
"""