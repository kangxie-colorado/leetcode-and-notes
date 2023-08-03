"""
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/?envType=study-plan&id=dynamic-programming-ii


can I use the same template??

own:
not: facing cooldown... 


cannot directly be applied to
maybe adding a new state: cooldown
"""


from functools import cache
from typing import List


class Solution_dp_fail:
    def maxProfit(self, prices: List[int]) -> int:

        own = [0, float('inf')]  # (profit, cost)
        notOwn = [0, 0]
        cooldown = [0,0]
        
        def choice(c1, c2, c3):
            return sorted([c1,c2,c3], key=lambda x: x[0]-x[1])[-1]

        for p in prices:

            prevOwnProfit, prevOwnCost = own
            prevNotProfit, _ = notOwn
            prevCDProfit, _ = cooldown

            # to own
            ownToOwn = own
            # this is limited by cooldown 
            notToOwn = [prevNotProfit, p]
            cooldownToOwn = [prevCDProfit, p]
            own = choice(ownToOwn, notToOwn, cooldownToOwn)

            # to not own
            notToNot = notOwn
            ownToNot = [prevOwnProfit+p-prevOwnCost, 0]
            cooldownToNot = [float('-inf'),0]
            notOwn = choice(notToNot, ownToNot, cooldownToNot)

            # to cool down
            ownToCooldown = [float('-inf'), 0]
            notToCooldown = [prevNotProfit, 0]
            cdTocd = cooldown
            cooldown = choice(ownToCooldown, notToCooldown, cdTocd)
            
        return max(own[0], notOwn[0], cooldown[0])


class Solution_dp_fail:
    def maxProfit(self, prices: List[int]) -> int:

        own = [0, float('inf'), 0]  # (profit, cost, cooldown)
        notOwn = [0, 0, 0]

        def choice(choices):
            return sorted(choices, key=lambda x: x[0]-x[1])[-1]

        for p in prices:

            prevOwnProfit, prevOwnCost, ownCooldown = own
            prevNotProfit, _, notCooldown = notOwn

            # to own
            ownToOwn = [prevOwnProfit, prevOwnCost, ownCooldown+1]
            # this is limited by cooldown
            notToOwn = [prevNotProfit, p]
            cooldownToOwn = [_, p]
            own = choice(ownToOwn, notToOwn, cooldownToOwn)

            ...

        return max(own[0], notOwn[0])


"""
nice try!
but I cannot get it to work yet.. 

how to factor in the cooldown in the state
cooldown in recursive will be reflected by idx... 

but how does that impact the decisions to own or not-to-own
cannot figure it out

the code won't work.. but leave them here
now let me think the recursive way first 

# state: own, sell, cooldown 
f(i, state) = max {
    own: max {
        sell: f(i+1, sell) + p-c
        or do nothing f(i+1, own)
    }

    sell: must cool down max {
        cooldown: f(i+1, cooldown) 
    }

    cooldown: 
        f(i+1, cooldown) # do nothing
        f(i+1, own, cost??)


}
"""


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        cooldown = 0
        own = 1
        sell = 2

        @cache
        def f(idx, state, cost):
            if idx >= len(prices):
                return 0
            
            if state == cooldown:
                return max(
                    f(idx+1, cooldown, cost), # continue cooldown, do-nothing
                    f(idx+1, own, prices[idx]) # buy at idx
                )
            elif state == own:
                return max (
                    f(idx+1, own, cost), # continue to own, do-nothing
                    f(idx+1, sell, 0) + prices[idx]-cost # sell at idx, update profit, and cost
                )
            else:
                # must cool down
                return f(idx+1, cooldown, 0)
        
        return f(0,cooldown,0)

"""
Runtime: 3637 ms, faster than 5.01% of Python3 online submissions for Best Time to Buy and Sell Stock with Cooldown.
Memory Usage: 585.1 MB, less than 5.79% of Python3 online submissions for Best Time to Buy and Sell Stock with Cooldown.

can I reduce the state variable to 2?
thus to reduce the calculations? I am not sure at all... but let me try

cost:-1 means just sell
cost:0 means cooldown
cost>0 means owning

(but 0 <= prices[i] <= 1000 )

so lets do this

cost:-2 means just sell
cost:-1 means cooldown
cost>0 means owning

there is no profit until you own and sell
so cost only will be contributing to final results when it is >=0 (own) and being sold
"""


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        cooldown = -1
        sell = -2

        @cache
        def f(idx, cost):
            if idx >= len(prices):
                return 0
            
            if cost == cooldown:
                return max(
                    f(idx+1, cost), # continue cooldown, do-nothing
                    f(idx+1, prices[idx]) # buy at idx
                )
            elif cost == sell:
                # must cool down
                return f(idx+1, cooldown)
            else:
                # own state
                return max (
                    f(idx+1, cost), # continue to own, do-nothing
                    f(idx+1, sell) + prices[idx]-cost # sell at idx, update profit, and cost
                )
        
        return f(0,cooldown)

"""
Runtime: 3657 ms, faster than 5.01% of Python3 online submissions for Best Time to Buy and Sell Stock with Cooldown.
Memory Usage: 584.9 MB, less than 5.79% of Python3 online submissions for Best Time to Buy and Sell Stock with Cooldown.

hmm.. still not great!!
ah.. maybe I can jump over the cooldown to simplify things
"""


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        @cache
        def f(idx, cost):
            if idx >= len(prices):
                return 0

            if cost>=0:
                # at idx, I already own (from some previous index)
                # continue to hold or sell
                # if I sell, I can jump next index, and go to idx+2
                return max(
                    f(idx+1, cost),
                    f(idx+2, -1) + prices[idx] - cost
                )
            else:
                # at idx, I have sold (from last index-2)
                # continue cooldown or buy (I can buy because cooldown day is skipped)
                return max(
                    f(idx+1, cost), 
                    f(idx+1, prices[idx])
                )


        return f(0, -1)

"""
Runtime: 2948 ms, faster than 5.47% of Python3 online submissions for Best Time to Buy and Sell Stock with Cooldown.
Memory Usage: 584.5 MB, less than 5.79% of Python3 online submissions for Best Time to Buy and Sell Stock with Cooldown.


wocao...
okay... let me see going back to bottom up
this cannot be using only two variables maybe.. it need two rows..

own to own: no change
own to not-own(sell): inherits the profit and plus new profit, cost to 0

not to not: no change
not to own(buy after cooldown): inherits the profit and cost to prices
    however.. this needs to looks across one col (that is the tricky part....)

one more extra variable or two rows..

"""


class Solution:
    def maxProfit(self, prices: List[int]) -> int:

        own = [0, prices[0]]  # (profit, cost)
        notOwn = [0, 0]
        prevNotOwn = [0,0]

        def choice(choices):
            return sorted(choices, key=lambda x: x[0]-x[1])[-1]

        for p in prices[1:]:
            ownToOwn = own 
            notToOwn = [prevNotOwn[0],p]
            
            notToNot = notOwn
            ownToNot = [own[0]+p-own[1], 0]

            prevNotOwn = notOwn
            own = choice([ownToOwn, notToOwn])
            notOwn = choice([notToNot, ownToNot])

        return max(own[0], notOwn[0])

""""
Runtime: 38 ms, faster than 95.15% of Python3 online submissions for Best Time to Buy and Sell Stock with Cooldown.
Memory Usage: 14.2 MB, less than 71.01% of Python3 online submissions for Best Time to Buy and Sell Stock with Cooldown.

probably I will totally forget what it is the solution 
"""

if __name__ == '__main__':
    s = Solution()
    print(s.maxProfit([48,12,60,93,97,42,25,64,17,56,85,93,9,48,52,42,58,85,81,84,69,36,1,54,23,15,72,15,11,94]))