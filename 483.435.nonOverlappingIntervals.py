"""
https://leetcode.com/problems/non-overlapping-intervals/

very much alike the ballon? I cannot see that...

okay https://leetcode.com/problems/non-overlapping-intervals/discuss/276056/Python-Greedy-Interval-Scheduling
this person explains it really well...

I got it now
will do this another time
"""


from typing import List


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x:x[1])

        removal=-1
        lastEnd=float('-inf')

        for s,e in intervals:
            if s>=lastEnd:
                lastEnd = e
            else:
                # must remove it
                removal+=1
        
        return removal

"""
turns out I solved in go.. but that logic was really messy
"""