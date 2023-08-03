"""
https://leetcode.com/problems/course-schedule-iv/?envType=study-plan&id=graph-ii


I tried topo sort map the course to its own layer but that messed up quickly
the unrelated course could belong to different layers.. and produce false positive dependency

then the hints say reachAble but I am thinking can I try bellman-ford
if the dist is inf.. then it is not related..
"""


from typing import List


class Solution:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        dist = [[float('inf')]*numCourses for _ in range(numCourses)]

        for i in range(numCourses):
            dist[i][i] = 0
        
        for i,j in prerequisites:
            dist[i][j] = 1
        
        for k in range(numCourses):
            for i in range(numCourses):
                for j in range(numCourses):
                    dist[i][j] = min(dist[i][j], dist[i][k]+dist[k][j])
        
        res = []
        for i,j in queries:
            if dist[i][j] != float('inf'):
                res.append(True)
            else:
                res.append(False)
        
        return res

"""
Runtime: 4764 ms, faster than 11.33% of Python3 online submissions for Course Schedule IV.
Memory Usage: 17.5 MB, less than 86.17% of Python3 online submissions for Course Schedule IV.

okay.. not sure the cycle..
"""