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

revisit 1/31/2023
Although I sovled I was struggling at best

now I am reading https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/discuss/135704/Detail-explanation-of-DP-solution
I gain some insights

the DP formula..
dp[k, i] = max(dp[k, i-1], prices[i] - prices[j] + dp[k-1, j-1]), j=[0..i-1]
    k: is the transaction 
    i: is selling on i-th day
e.g. dp[2,8]: selling 2nd time on 8th day
My previous DP thoughts didn't even include this k.. transaction
I was think/struggling/wriggling how to combine two one-transaction DP into two-transactions
(but kind of to the same effect)

now understand this formula..
    k-th transaction's profit on i-th day will be 
        1. either not doing(selling) it on i-th day (doing it on i-1th day)
        2. or selling it on i-th day.. that means 
            buying can happen on j <- (0...i-1) day.. (? why this can go back to 0.. if k==2, it can only start from day3.. guess not changing results)
            so this transaction's profit will be prices[i]-prices[j]
            the previous transaction will be  dp[k-1, j-1] (buying at j-th day.. sold at most happened on j-1th day.. it will be inherited)


let me code this up.. guess it will TLE
"""


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        # dp[0][*] will be feed
        # dp[1][*] selling 1 at i-th day
        # dp[2][*] selling 2 at i-th day
        dp = [[0]*n for _ in range(3)] 

        for k in range(1,3):
            for i in range(1, n): # i starts with i.. because you can only sell at 2nd day (index-1)
                minCost = prices[0]
                for j in range(1, i): 
                    # this is easy to understand, up to i-th day (index-1 means 2nd day)
                    # the min cost 
                    # hmm.. how to understand this?
                    # if it is that buy/sell once: the it will just be prices[j]
                    # now enter the possible previous transaction 
                    # aha.. the cost is this ”price minus previous profit“....
                    #   hmm.. makes sense.. that consolidate two transactions into 1
                    #   hmm.. MF.. the secrect is this.. 
                    #   also.. this will be in math's sense equal to above formula...
                    minCost = min(minCost, prices[j]-dp[k-1][j-1]) # current cost - previous profit.. it could go negative for sure..
                dp[k][i] = max(dp[k][i-1], prices[i]-minCost)

        return dp[2][n-1]
"""
the first transcation's profit is factored into the cost for 2nd transaction -- that's kind of natural and clever

think this will TLE
202 / 214 test cases passed. and TLE.. not bad at all

the first jump to simplify is hard to understand let me see
"""


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        # dp[0][*] will be feed
        # dp[1][*] selling 1 at i-th day
        # dp[2][*] selling 2 at i-th day
        dp = [[0]*n for _ in range(3)]

        for k in range(1, 3):
            minCost = prices[0]
            for i in range(1, n):  # i starts with i.. because you can only sell at 2nd day (index-1)
                # this optimization seems hard to understand?
                # but it is kind of natural 
                # 1. minCost keep track of up-to i-1, the minCost 
                # 2. then if I buy at i-th day.. the minCost is current prices minu preivous profit
                # BUT.. if I buy at i-th day, I cannot sell at i-th day.. 
                # how to reconcile that
                # let me see... if prices[i]-dp[k-1][i-1] happens to be minCost
                # then sell at this day.. is like giving up one transaction (it will not affect results)
                # but I wonder if I can change to prices[i-1] (yeah.. it still works) (next submission)
                # BTW, change to i-2 it went wrong.. of course
                minCost = min(minCost, prices[i]-dp[k-1][i-1])
                dp[k][i] = max(dp[k][i-1], prices[i]-minCost)

        return dp[2][n-1]

"""
Runtime: 1464 ms, faster than 56.08% of Python3 online submissions for Best Time to Buy and Sell Stock III.
Memory Usage: 28.8 MB, less than 49.25% of Python3 online submissions for Best Time to Buy and Sell Stock III.
"""


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        # dp[0][*] will be feed
        # dp[1][*] selling 1 at i-th day
        # dp[2][*] selling 2 at i-th day
        dp = [[0]*n for _ in range(3)]

        for k in range(1, 3):
            minCost = prices[0]
            for i in range(1, n):  # i starts with i.. because you can only sell at 2nd day (index-1)

                minCost = min(minCost, prices[i-1]-dp[k-1][i-1]) # using i-1 to calculate the cose
                dp[k][i] = max(dp[k][i-1], prices[i]-minCost)

        return dp[2][n-1]

"""
Runtime: 1460 ms, faster than 56.44% of Python3 online submissions for Best Time to Buy and Sell Stock III.
Memory Usage: 28.7 MB, less than 70.25% of Python3 online submissions for Best Time to Buy and Sell Stock III.

the key insight to this part is minCost actually tracks minCost up to [i-1]

swap row/column doesn't change results
but you need to deal with the minCost for each one.. 

"""


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        # dp[0][*] will be feed
        # dp[1][*] selling 1 at i-th day
        # dp[2][*] selling 2 at i-th day
        dp = [[0]*n for _ in range(3)]
        # for each transaction the minCost
        minCost = [prices[0]]*3
        for i in range(1, n):
            for k in (1,2):
                # swap order.. this produces new meaning?
                # and kind of more clear
                # on i-th, k'th txn's cost will be prices[i] (or i-1 I think) minus previous profit
                minCost[k] = min(minCost[k], prices[i-1] - dp[k-1][i-1])
                dp[k][i] = max(dp[k][i-1], prices[i]-minCost[k])
        return dp[2][n-1]

"""
Runtime: 1546 ms, faster than 51.72% of Python3 online submissions for Best Time to Buy and Sell Stock III.
Memory Usage: 28.8 MB, less than 49.25% of Python3 online submissions for Best Time to Buy and Sell Stock III.

                minCost[k] = min(minCost[k], prices[i-1] - dp[k-1][i-1])
                                                    ^ using i or i-1 both right

compact because i-th only depends on i-1

"""


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        dp = [0]*3
        dp2 = [0]*3
        minCost = [prices[0]]*3
        minCost2 = [prices[0]]*3

        for i in range(1,n):
            for k in (1,2):
                
                minCost[k] = min(minCost[k], prices[i-1] - dp[k-1])
                dp[k] = max(dp[k], prices[i]- minCost[k])
                # using i-1 or i both right? nope!
                

                minCost2[k] = min(minCost2[k], prices[i] - dp2[k-1])
                dp2[k] = max(dp2[k], prices[i] - minCost2[k])

            print(prices[i])
            print(minCost, "      ", minCost2)
            print(dp, "      ", dp2)
            print()
        return dp[2]

"""
huh.. this will diff between using i-1 and i to calculate cost 
if I use i-1.. it got bigger-by-1 results for positive profit???

why? let me see
hmm.. subtle.. let me go back to above to print debug
"""

# for debug i-1 vs i
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        # dp[0][*] will be feed
        # dp[1][*] selling 1 at i-th day
        # dp[2][*] selling 2 at i-th day
        dp = [[0]*n for _ in range(3)]
        dp2 = [[0]*n for _ in range(3)]
        # for each transaction the minCost
        minCost = [prices[0]]*3
        minCost2 = [prices[0]]*3
        for i in range(1, n):
            for k in (1, 2):
                # swap order.. this produces new meaning?
                # and kind of more clear
                # on i-th, k'th txn's cost will be prices[i] (or i-1 I think) minus previous profit
                minCost[k] = min(minCost[k], prices[i-1] - dp[k-1][i-1])
                dp[k][i] = max(dp[k][i-1], prices[i]-minCost[k])

                minCost2[k] = min(minCost2[k], prices[i] - dp2[k-1][i-1])
                dp2[k][i] = max(dp2[k][i-1], prices[i]-minCost2[k])
            print(prices[i])
            print(dp[0], "    ", dp2[0])
            print(dp[1], "    ", dp2[1])
            print(dp[2], "    ", dp2[2])
            print(minCost, "                    ", minCost2)
            print()


        return dp[2][n-1]

"""
okay.. with this example 
    print(s.maxProfit(prices = [3,3,5,0,0,3,1,4]))


3
[0, 0, 0, 0, 0, 0, 0, 0]      [0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0]      [0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0]      [0, 0, 0, 0, 0, 0, 0, 0]
[3, 3, 3]                      [3, 3, 3]

5
[0, 0, 0, 0, 0, 0, 0, 0]      [0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 2, 0, 0, 0, 0, 0]      [0, 0, 2, 0, 0, 0, 0, 0]
[0, 0, 2, 0, 0, 0, 0, 0]      [0, 0, 2, 0, 0, 0, 0, 0]
[3, 3, 3]                      [3, 3, 3]

0
[0, 0, 0, 0, 0, 0, 0, 0]      [0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 2, 2, 0, 0, 0, 0]      [0, 0, 2, 2, 0, 0, 0, 0]
[0, 0, 2, 2, 0, 0, 0, 0]      [0, 0, 2, 2, 0, 0, 0, 0]
[3, 3, 3]                      [3, 0, -2]

at day 4, after first sale.. the cost for k=2 can be -2 (the profit of k=1 txn) 
which seems correct actually.. 

the cost being 3.. seems not correct.. but somehow it doesn't change the results
because the buy/sell cannot happen on one day...

also intersting to notice that cost for k=1 becomes 0.... (that's actually the price on 4-th day hitting 0)

haha.. my notice of using i-1 is actually logical wrong
thinking the 1-D

3 2 1 0
    ^ at here.. the cost if using i-1, it will be 2.. the profit will be -1 (but that was masked by max(0,-1))
so okay.. deal with using prices[i]

if at i-th day, the prices is lowest.. that means we just cannot sell on that day (otherwise loss)
"""


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        dp = [0]*3
        dp2 = [0]*3
        minCost = [prices[0]]*3

        for i in range(1, n):
            for k in (1, 2):
                minCost[k] = min(minCost[k], prices[i] - dp[k-1])
                dp[k] = max(dp[k], prices[i] - minCost[k])

        return dp[2]
"""
Runtime: 1385 ms, faster than 63.02% of Python3 online submissions for Best Time to Buy and Sell Stock III.
Memory Usage: 28.9 MB, less than 49.25% of Python3 online submissions for Best Time to Buy and Sell Stock III.

and finally the natural way
"""


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        n = len(prices)
        cost1=cost2=float('inf')
        profit1=profit2=0

        for i in range(n):
            cost1 = min(cost1, prices[i])
            profit1 = max(profit1, prices[i]-cost1)
            # integrate privious profit into the cost.. can be negative
            cost2 = min(cost2, prices[i]-profit1)
            profit2 = max(profit2, prices[i]-cost2)

        return profit2

"""
Runtime: 1102 ms, faster than 92.53% of Python3 online submissions for Best Time to Buy and Sell Stock III.
Memory Usage: 28.9 MB, less than 36.05% of Python3 online submissions for Best Time to Buy and Sell Stock III.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.maxProfit(prices = [3,3,5,0,0,3,1,4]))
    print(s.maxProfit(prices = [3,1,6,2,0,3,1,4]))
    print(s.maxProfit(prices = [1,2,3,4,5]))
    print(s.maxProfit(prices = [7,6,4,3,1]))