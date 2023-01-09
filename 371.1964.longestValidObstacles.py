"""
https://leetcode.com/problems/find-the-longest-valid-obstacle-course-at-each-position/

yeah I also figured it out this is a LIS problem

"""


import bisect
from typing import List


class Solution:
    def longestObstacleCourseAtEachPosition(self, obstacles: List[int]) -> List[int]:
        lis = [obstacles[0]]
        res = [1]
        for ob in obstacles[1:]:
            if ob >= lis[-1]:
                lis.append(ob)
                res.append(len(lis))
            else:
                idx = bisect.bisect_right(lis, ob)
                lis[idx] = ob
                res.append(idx+1)

        return res


"""
Runtime: 3960 ms, faster than 31.04% of Python3 online submissions for Find the Longest Valid Obstacle Course at Each Position.
Memory Usage: 29.1 MB, less than 91.38% of Python3 online submissions for Find the Longest Valid Obstacle Course at Each Position.
"""