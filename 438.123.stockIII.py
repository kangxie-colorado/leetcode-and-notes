"""
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/

not quite sure how to do
but buy/sell once is trivial -- just keep min cost and update the max profit I can get

so I think if I can divide and conqure or maybe dp
   [3,3,5,0,0,3,1,4]
    0 1 2 3 4 5 6 7 
0   0
1     0
2       0
3         0
4           0
5             0
6               0
7                 0

if in such a DP table, dp[i][j] represents max profit of buy/sell once.. 
when i>=j, 0.. so only the upper half 

then buying twice can be 
max(dp[i][k] + dp[k][j]) k from i to j, inclusive.. 

but the data is big
1 <= prices.length <= 10^5

O(n**2) cannot cut it... 

maybe divide conqure,, which is T(N) = 2 * T(N/2) + some-processing?
nah.. still not divide conqure.. it has to be k from i to j.. O(n**2)

from the data scope.. I guess it at most can be some k*O(n)
maybe own/not-own
          [3,3,5,0,0,3,1,4]
           0 1 2 3 4 5 6 7 
own        
not-own

what is the states?
dp[i][*] (txnLeft, p,c)

then when own->not-own.. that is sell
not-own->own... that is buy

"""


from typing import List


"""
maybe I can use 6 or 5 rows 
(first row being not-own at all.. which is not informational so no need)

            3 1 6 2 0 5 1 4
not-own-1
own-1
sell-1
not-own-2
own-2
sell-2

not-own-1:
    (0,0) all the way.. not needed really
own-1: 
    focus on the cost, the profit is always 0
sell-1: 
    can only come from own-1, price - (own-1[cost]), and cost becomes 0

not-own-2: like the idle time, 
    comes from sell-1 or itself... which ever profit-cost is bigger
own-2: 
    comes from sell-1, not-own-2 or itself... which ever profit-cost is bigger
sell-2:
    can only come from own-2
    
in the process, update the res as it goes. 
and obviously it only needs last column.. so a variable if carefully maintained would be enough 
"""

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        res = 0
        negInf = float('-inf')
        
        own1 = [0,prices[0]]
        sell1 = [negInf, 0]
        idle = [negInf, 0]
        own2 = [negInf, 0]
        # sell2 = [negInf, 0] # not depended on, so just to update the res

        for i, price in enumerate(prices):
            
            # because of the dependencies, I update from bottom to top
            # i.e. from sell2 to own1
            if i>=3:
                # only from 4-th day, sell2 becomes possible
                res = max(res, price - own2[1] + own2[0])
            if i>=2:
                # only from 3-rd day, own2 becomes possible
                fromSell1P,fromSell1C = sell1[0], price
                fromIdleP, fromIdleC = idle[0], price 

                if fromSell1P-fromSell1C > fromIdleP-fromIdleC:
                    candiP, candiC = fromSell1P, fromSell1C
                else:
                    candiP, candiC = fromIdleP, fromIdleC
                
                if candiP-candiC > own2[0]-own2[1]:
                    own2 = [candiP, candiC]
                
                # also only from 3-rd day, idle becomes possible
                # it is computed as above already
                idle = candiP,candiC

            if i>=1:
                # only from 2-nd day, sell1 becomes possible
                # it can only come from own1
                sell1 = [price - own1[1], 0]
                res = max(res, sell1[0])
            
            # i>=0, update own1's cost
            own1 = [0, min(own1[1], price)]
        return res

"""
Runtime: 1320 ms, faster than 70.90% of Python3 online submissions for Best Time to Buy and Sell Stock III.
Memory Usage: 29 MB, less than 36.48% of Python3 online submissions for Best Time to Buy and Sell Stock III.

"""
if __name__ == '__main__':
    s = Solution()
    print(s.maxProfit(prices = [3,3,5,0,0,3,1,4]))
    print(s.maxProfit(prices = [3,1,6,2,0,3,1,4]))
    print(s.maxProfit(prices = [1,2,3,4,5]))
    print(s.maxProfit(prices = [7,6,4,3,1]))