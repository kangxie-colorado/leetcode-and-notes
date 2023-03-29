"""
https://leetcode.com/problems/maximum-profit-in-job-scheduling/

I have 12 minutes left for today.. and I intend to respect that..
so give it up for this one for today.. pick it up tomorrow.. 


ok.. it was the day after tomorrow I picked it up
my priority and energy flow needs adjustment so anyway.. 

slow down is okay
but still keep it warm.. 

so this problem is very much like 1751 without the limitation of k
"""


import bisect
from functools import cache
from typing import List


class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        startEndProfit = sorted([(s,e,p )for s,e,p in zip(startTime,endTime,profit)])

        @cache
        def schedule(idx):
            if idx==len(startEndProfit):
                return 0
            
            notTaking = schedule(idx+1)

            # find out the next job to schedule if taking current one
            searchItem = (startEndProfit[idx][1], 0, 0)
            nextJobIdx = bisect.bisect_left(startEndProfit, searchItem)
            taking = schedule(nextJobIdx) + startEndProfit[idx][2]    

            return max(notTaking, taking)
        
        return schedule(0)

"""
Runtime: 619 ms, faster than 59.73% of Python3 online submissions for Maximum Profit in Job Scheduling.
Memory Usage: 109 MB, less than 7.89% of Python3 online submissions for Maximum Profit in Job Scheduling.

this could be converted to bottom up as well
the last results can be stored in dp[0] or dp[n].. depending how you scan and how to leap forward

let me just follow the same idea as above, storing it in dp[0]
therefore, dp[i] = max(
    dp[i+1], # not taking ith
    dp[idx]+values[i] # taking ith and leap to idx.. 
)

dp[n] = 0
so it is actually a one dimension dp, i.e. dp[i] only depends on dp[i+1] and dp[idx]

the idx can be pre-computed as well

"""


class Solution:
    def jobScheduling(self, startTime: List[int], endTime: List[int], profit: List[int]) -> int:
        # start,end,profit,nextEvent
        startEndProfit = sorted([[s, e, p, -1] 
                                for s, e, p in zip(startTime, endTime, profit)])

        for i, event in enumerate(startEndProfit):
            search = [event[1],0,0,-1]
            startEndProfit[i][3] = bisect.bisect_left(startEndProfit, search)
        
        n = len(startTime)
        dp = [0] * (n+1)

        for i in range(n-1,-1,-1):
            dp[i] = max(dp[i+1], startEndProfit[i][2]+dp[startEndProfit[i][3]])

        return dp[0]


"""
Runtime: 568 ms, faster than 73.98% of Python3 online submissions for Maximum Profit in Job Scheduling.
Memory Usage: 29.2 MB, less than 47.61% of Python3 online submissions for Maximum Profit in Job Scheduling.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.jobScheduling(startTime = [1,2,3,3], endTime = [3,4,5,6], profit = [50,10,40,70]))
    print(s.jobScheduling(startTime = [1,2,3,4,6], endTime = [3,5,10,6,9], profit = [20,20,100,70,60]))