"""
I think this is a line sweep problem
just need to focus on the start/end point, rather than focus on the intervals

just need to record at which point the max overlapping

to do that, I need to sort start, end together but with some marking
"""

from collections import defaultdict
from typing import List


class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        
        starts = [(start,1) for start, _ in intervals]
        ends = [(end, -1) for _,end in intervals]
        times = sorted(starts+ends)

        res = 0
        overlap = 0
        for _,score in times:
            overlap += score
            res = max(res, overlap)
        
        return res
        
        