"""
https://leetcode.com/problems/course-schedule-ii/

okay.. this is the sort part

I vaguely knew this algorithm but not 100% sure
so first I need to find the node that is without a prerequisit? and use that as the start?
"""


from collections import defaultdict, deque
from typing import List


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        adjSets = defaultdict(set)
        for course, pre in prerequisites:
            adjSets[course].add(pre)

        res = []
        def dfs(course, path):
            if course in res:
                return True
            if course in path:
                return False
            
            for pre in adjSets[course]:
                if not dfs(pre, path.union({course})):
                    return False
        
            res.append(course)
            return True
        
        for c in range(numCourses):
            if not dfs(c, set()):
                return []
        return res

"""
Runtime: 569 ms, faster than 5.02% of Python3 online submissions for Course Schedule II.
Memory Usage: 102.3 MB, less than 5.18% of Python3 online submissions for Course Schedule II.

let me use some extra memory and see if that can save time
"""


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        adjSets = defaultdict(set)
        for course, pre in prerequisites:
            adjSets[course].add(pre)

        res = []
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
            res.append(course)
            return True

        for c in range(numCourses):
            if not dfs(c, set()):
                return []
        return res

"""
Runtime: 430 ms, faster than 5.94% of Python3 online submissions for Course Schedule II.
Memory Usage: 102.6 MB, less than 5.18% of Python3 online submissions for Course Schedule II.

so anyway, the key is to dfs to the end and append the finished course to res
it can happen in any possible order
"""


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        adjSets = defaultdict(set)
        for course, pre in prerequisites:
            adjSets[course].add(pre)

        res = []
        visited = [0]*numCourses

        def dfs(course):
            if visited[course] == 2:
                return True
            if visited[course] == 1:
                return False

            # add to path
            visited[course] = 1

            for pre in adjSets[course]:
                if not dfs(pre):
                    return False
            
            visited[course] = 2
            res.append(course)
            return True

        for c in range(numCourses):
            if not dfs(c):
                return []
        return res

"""
Runtime: 138 ms, faster than 43.94% of Python3 online submissions for Course Schedule II.
Memory Usage: 17.9 MB, less than 5.18% of Python3 online submissions for Course Schedule II.

okay.. there is that bfs solution
when the incoming link is 0.. adding to queue.. 
this is the bfs.. hmm.. like that LIS in matrix.. 

I didn't recognize this very naturally 
maybe this is quicker

let me give a try 
"""


class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        adjSets = defaultdict(set)
        incomingLinks = [0]*numCourses
        for course, pre in prerequisites:
            adjSets[pre].add(course)
            incomingLinks[course]+=1
        
        bfsQ = deque()
        for c in range(numCourses):
            if incomingLinks[c] == 0:
                bfsQ.append(c)
        
        res = []
        while bfsQ:
            l = len(bfsQ)
            while l:
                c = bfsQ.popleft()
                res.append(c)
                for dep in adjSets[c]:
                    incomingLinks[dep] -= 1
                    if incomingLinks[dep] == 0:
                        bfsQ.append(dep)
                l-=1
        return res if len(res)==numCourses else []

"""
Runtime: 105 ms, faster than 73.64% of Python3 online submissions for Course Schedule II.
Memory Usage: 15.4 MB, less than 85.23% of Python3 online submissions for Course Schedule II.

this is important.. if all is sorted.. the res should be full otherwise it means it cannot be sorted
        return res if len(res)==numCourses else []

interesting! it doesn't need to detect the cycle? 
it only append to queue when incoming becomes zero

when there is a cycle
0 --> 1 and 1 ---> 0

what happens?
there will be no queue to start.. 

in such case [[1,0],[1,2],[0,1]]
2 will be processed and 1 will still have an incoming link.. so not in queue anyway..

interesting..

    
"""

if __name__ == '__main__':
    s = Solution()
    print(s.findOrder(numCourses=1, prerequisites=[]))
    print(s.findOrder(numCourses=2, prerequisites=[[1, 0]]))
    print(s.findOrder(numCourses=4, prerequisites=[
          [1, 0], [2, 0], [3, 1], [3, 2]]))

    print(s.findOrder(numCourses=2, prerequisites=[[1, 0], [0, 1]]))
    print(s.findOrder(numCourses=6, prerequisites=[
          [1, 0], [0, 2], [3, 4], [5, 3]]))
