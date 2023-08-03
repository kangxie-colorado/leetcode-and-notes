"""
https://leetcode.com/problems/course-schedule/

this is just cycle detection in directed graph 
we can just use the direction to mean depends on
[0,1] means 0 depends on 1... 

if you say its a cycle detection, where to start the traversal?
topological sort just scan every node and see if it is scanned?

yeah, so when the checked courses reaches n.. it can
"""


from collections import defaultdict, deque
from typing import List


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adjSets  = defaultdict(set)
        for course, pre in prerequisites:
            adjSets[course].add(pre)
        
        visited = set()
        def dfs(course, path):
            if course in visited:
                return True
            if course in path:
                return False
            
            for pre in adjSets[course]:
                if not dfs(pre, path.union({course})):
                    return False
            
            visited.add(course)
            return True
        
        for course in range(numCourses):
            if not dfs(course, set()):
                return False
        
        return True

"""
Runtime: 156 ms, faster than 36.92% of Python3 online submissions for Course Schedule.
Memory Usage: 102.5 MB, less than 5.14% of Python3 online submissions for Course Schedule.

okay.. it was all by memeory 
I of course can use =1 to mean in path, =2 to mean processed
"""


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adjSets = defaultdict(set)
        for course, pre in prerequisites:
            adjSets[course].add(pre)

        # 0: non-visited
        # 1: in path
        # 2: visited
        status = [0] * numCourses

        def dfs(course):
            if status[course] == 2:
                return True
            if status[course] == 1:
                return False

            # add to path
            status[course] = 1
            for pre in adjSets[course]:
                if not dfs(pre):
                    return False

            status[course] = 2
            return True

        for course in range(numCourses):
            if not dfs(course):
                return False

        return True

"""
Runtime: 108 ms, faster than 57.26% of Python3 online submissions for Course Schedule.
Memory Usage: 17.6 MB, less than 9.56% of Python3 online submissions for Course Schedule

let me also do this in bfs way
"""


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adjSets = defaultdict(set)
        incomingLinks = [0] * numCourses
        for course, pre in prerequisites:
            adjSets[course].add(pre)
            incomingLinks[pre] += 1
        
        bfsQ = deque()
        for c in range(numCourses):
            if incomingLinks[c] == 0:
                bfsQ.append(c)
        
        sorted = []
        while bfsQ:
            l = len(bfsQ)
            while l:
                c = bfsQ.popleft()
                sorted.append(c)

                for pre in adjSets[c]:
                    incomingLinks[pre] -= 1
                    if incomingLinks[pre] == 0:
                        bfsQ.append(pre)
                l-=1
        return len(sorted) == numCourses

"""
Runtime: 96 ms, faster than 91.65% of Python3 online submissions for Course Schedule.
Memory Usage: 15.4 MB, less than 87.29% of Python3 online submissions for Course Schedule.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.canFinish(numCourses=2, prerequisites=[[1, 0]]))
    print(s.canFinish(numCourses=2, prerequisites=[[1, 0], [0, 1]]))
    print(s.canFinish(numCourses=6, prerequisites=[[1, 0], [0, 2], [3,4], [5,3]]))
            
            