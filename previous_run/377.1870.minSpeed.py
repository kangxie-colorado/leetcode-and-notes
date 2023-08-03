"""
https://leetcode.com/problems/minimum-speed-to-arrive-on-time/?envType=study-plan&id=binary-search-ii



"""


from typing import List


class Solution:
    def minSpeedOnTime(self, dist: List[int], hour: float) -> int:
        def canArrive(spd):
            time = 0
            for d in dist[:-1]:
                time += (d-1)//spd + 1

            time += dist[-1]/spd
            return time <= hour

        l, r = 1, 10000001
        while l < r:
            m = l+(r-l)//2
            if canArrive(m):
                r = m
            else:
                l = m+1
        return l if l < 10000001 else -1

"""
Runtime: 2788 ms, faster than 94.61% of Python3 online submissions for Minimum Speed to Arrive on Time.
Memory Usage: 28.2 MB, less than 63.17% of Python3 online submissions for Minimum Speed to Arrive on Time.
"""