"""
https://leetcode.com/problems/minimum-interval-to-include-each-query/

sort intervals and queries 
then adding the intervals containsing the q to a heap, sort it by length and interval-right 

then peak into the heap.. if the top meets the queries, then use it... but don't pop it yet
otherwise, if it is already out of scope.. pop it
"""


import heapq
from typing import List


class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        # sort is essential and can give us the break when q has exceeded right(see loop below)
        intervals.sort()
        queries = sorted([(q,i) for i,q in enumerate(queries)])

        res = [-1 for _ in queries]
        h = []
        intervalIdx = 0
        for q,i in queries:
            while intervalIdx < len(intervals):
                left,right = intervals[intervalIdx]
                # cannot use this test
                # if not left<=q<=right:
                # because when q > right.. it could be next interval  7 vs 4-5, 5-8
                # 4-5 doesn't contain it.. 5-8 does
                if left > q:
                    # then for next q, it can pick up right where it was left off
                    break

                # so the rule now becomes
                # if left > q.. this interval is too big already.. break 
                # pass above, then if right>=q... this interval contains this q
                if right >= q:
                    heapq.heappush(h, (right-left+1, right))
                # only when interval is valid, increment idx
                # this comment is wrong.. also increment when interval is too small
                intervalIdx += 1
            
            # now, time to look for a valid interval 
            while h and h[0][1]<q:
                heapq.heappop(h)
            
            res[i] = h[0][0] if h else -1

        
        return res 


"""
Runtime: 5793 ms, faster than 5.17% of Python3 online submissions for Minimum Interval to Include Each Query.
Memory Usage: 59 MB, less than 17.90% of Python3 online submissions for Minimum Interval to Include Each Query.

aslightly simplified version
"""    


class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        # sort is essential and can give us the break when q has exceeded right(see loop below)
        intervals.sort()
        queries = sorted([(q, i) for i, q in enumerate(queries)])

        res = [-1 for _ in queries]
        h = []
        intervalIdx = 0
        for q, i in queries:
            while intervalIdx < len(intervals):
                left, right = intervals[intervalIdx]

                if left <= q <= right:
                    heapq.heappush(h, (right-left+1, right))
                if q < left:
                    break
                # increment idx when the interval is valid.. and too small
                intervalIdx += 1

            # now, time to look for a valid interval
            while h and h[0][1] < q:
                heapq.heappop(h)

            res[i] = h[0][0] if h else -1

        return res
            
if __name__ == '__main__':
    s = Solution()
    print(s.minInterval([[4, 5], [5, 8], [1, 9], [8, 10], [1, 6]], [7, 9, 3, 9, 3]))



