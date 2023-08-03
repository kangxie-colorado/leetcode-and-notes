"""
https://leetcode.com/problems/stone-game-iii/?envType=study-plan&id=dynamic-programming-iii

this seems not very complicated
"""


from functools import cache
from typing import List


class Solution:
    def stoneGameIII(self, stoneValue: List[int]) -> str:
        n = len(stoneValue)

        @cache
        def f(idx):
            if idx>=n:
                return 0,0
            
            diff = float('-inf')
            mine=yours=0
            for i in range(1,4):
                currGain = sum(stoneValue[idx:idx+i])
                yourGain, subGain = f(idx+i)
                netDiff = currGain+subGain-yourGain
                if netDiff > diff:
                    diff = netDiff
                    mine, yours = currGain+subGain, yourGain
            
            return mine,yours
        
        alice,bob=f(0)
        if alice>bob:
            return 'Alice'
        elif alice<bob:
            return 'Bob'
        else:
            return 'Tie'

"""
failed at 
[-1,-2,-3]

hmm... 
okay.. the base isn't right..

the suffix sum could be negative or contain negative values.. 
it is not necessarily optimal to just take all 

Runtime: 3823 ms, faster than 41.75% of Python3 online submissions for Stone Game III.
Memory Usage: 319.5 MB, less than 9.63% of Python3 online submissions for Stone Game III.
"""


class Solution:
    def stoneGameIII(self, stoneValue: List[int]) -> str:
        n = len(stoneValue)

        @cache
        def f(idx):
            if idx >= n:
                return 0, 0

            diff = float('-inf')
            mine = yours = 0
            currGain = 0
            for i in range(3):
                if idx+i < n:
                    currGain += stoneValue[idx+i]
                    yourGain, subGain = f(idx+i+1)
                    netDiff = currGain+subGain-yourGain
                    if netDiff > diff:
                        diff = netDiff
                        mine, yours = currGain+subGain, yourGain

            return mine, yours

        alice, bob = f(0)
        if alice > bob:
            return 'Alice'
        elif alice < bob:
            return 'Bob'
        else:
            return 'Tie'

if __name__ == '__main__':
    s = Solution()
    print(s.stoneGameIII( [1,2,3,7]))
    print(s.stoneGameIII( [1,2,3,-9]))
    print(s.stoneGameIII( [1,2,3,6]))