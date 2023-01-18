"""
https://leetcode.com/problems/most-profit-assigning-work/

if I put the difficulty,profit together and sort ?
then for each work.. I find the most profit job under-or-equal his abiliity?

the example tells me profit is not necessarily higher when the difficulty is higher
can I override?

let me say, using pair (diff, profit)
(1,10) (2,5) => I can overwrite to (1,10), (2,10)

yeah.. I can give a try 


"""


from bisect import bisect
from typing import List


class Solution:
    def maxProfitAssignment(self, difficulty: List[int], profit: List[int], worker: List[int]) -> int:

        diffProfit = sorted([(diff,prof) for diff,prof in zip(difficulty, profit)])

        maxProfit = diffProfit[0][1]
        for i in range(len(diffProfit)):
            diff, prof = diffProfit[i]
            if prof < maxProfit:
                diffProfit[i] = (diff, maxProfit)
            else:
                maxProfit = prof 
        
        res = 0
        for w in worker:
            idx = bisect.bisect_right(diffProfit, (w,100001))
            if idx > 0:
                res += diffProfit[idx-1][1]
        return res

"""
Runtime: 377 ms, faster than 87.44% of Python3 online submissions for Most Profit Assigning Work.
Memory Usage: 17.1 MB, less than 70.18% of Python3 online submissions for Most Profit Assigning Work.
"""