"""
https://leetcode.com/problems/find-right-interval/

seem like a straightforward binary searching of end in start array

aha.. the intervals are not sorted... 
so I can sort it just carry the index 
"""


import bisect
from typing import List


class Solution:
    def findRightInterval(self, intervals: List[List[int]]) -> List[int]:

        startAndIdxs = sorted([(intv[0], idx)
                              for idx, intv in enumerate(intervals)])
        res = []
        for _, end in intervals:
            idx = bisect.bisect_left(startAndIdxs, (end, 0))
            if idx < len(startAndIdxs) and startAndIdxs[idx][0] >= end:
                res.append(startAndIdxs[idx][1])
            else:
                res.append(-1)

        return res

"""
Runtime: 307 ms, faster than 85.05% of Python3 online submissions for Find Right Interval.
Memory Usage: 20.2 MB, less than 58.79% of Python3 online submissions for Find Right Interval.
"""