"""
https://leetcode.com/problems/best-time-to-buy-and-sell-stock/?envType=study-plan&id=data-structure-i

did this many times but still don't see the solution very quick
I knew I did something like a template for buy/sell stock w/ w/o restrictions 

the key is to keep two states (own a stock, or not own a stock) and transition between 
and for each day/state, I maintain maybe a profit and a cost
but for this one, there is a simpler shortcut

so I think it is as follow
1. profit is basically maintained after each day
2. at a point, the profit I can get is the price-cost (cost is up to me, the mini cost )
that gives me the idea.. just need to see the mini-cost before me
"""


from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:

        profit = 0
        cost = float('inf')

        for p in prices:
            profit = max(profit, p-cost)
            cost = min(cost, p)
        return profit 

"""
Runtime: 2038 ms, faster than 30.98% of Python3 online submissions for Best Time to Buy and Sell Stock.
Memory Usage: 25.1 MB, less than 35.57% of Python3 online submissions for Best Time to Buy and Sell Stock.

hopefully with me hammering down my fundmentals, it becomes solid
"""