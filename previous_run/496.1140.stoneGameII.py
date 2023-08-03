"""
https://leetcode.com/problems/stone-game-ii/

f(idx,M)
    represent at idx pile, with M, maxNumber of piles I can get.. remeber the next move is not mine
    it will be 

    min(
        f(idx+1,max(1,M)) + sum[idx:idx+1]
        f(idx+2,max(2,M)) + sum[]
        ..
        f(idx+k, max(k,M)) k<=min(n-idx,2M)
    )

    min of max? yes.. for me to win, you need to take the least.. so yeah it should be min
    base case.. 
        idx==n: return 0

okay.. the scoring algorithm isn't right yet


"""


from functools import cache
from typing import List


class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        n = len(piles)
        summ = [0] * (n+1)
        for i in range(1,n+1):
            summ[i] = summ[i-1] + piles[i-1]

        def f(idx,M):
            if idx >= len(piles):
                return 0
            
            res = float('inf')
            for x in range(1,min(2*M, n)+1):
                if idx+x < n+1:
                    res = min(res, f(idx+x, max(M,x)) + summ[idx+x] - summ[idx] ) 

            return res
        
        return f(0,1)

"""
okay.. the scoring algorithm isn't right yet

            res = float('inf')
            for x in range(1,min(2*M, n)+1):
                if idx+x < n+1:
                    res = min(res, f(idx+x, max(M,x)) + summ[idx+x] - summ[idx] ) 
                        ^ not super right
                            summ[]-summ[] part is my score.. 
                            probably should do a negative/positive minus/add
                        

"""


class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        n = len(piles)
        summ = [0] * (n+1)
        for i in range(1, n+1):
            summ[i] = summ[i-1] + piles[i-1]

        @cache
        def f(idx, M):
            if idx >= n:
                return 0,0
            
            if idx+2*M>=n:
                return summ[-1] - summ[idx],0

            diff = float('-inf')
            mine=yours=0
            for x in range(1, min(M*2,n)+1):
                if idx+x < n+1:
                    currGain = summ[idx+x] - summ[idx]
                    yourGain,subGain = f(idx+x, max(M, x))
                    netDiff = currGain + subGain - yourGain
                    # maxmize my gain and minimize your gain, but they must interact (example 1)
                    # meaning maxmize myGain-yourGain
                    if netDiff > diff:
                        diff = netDiff
                        mine, yours = currGain+subGain, yourGain
            
            # print(idx,M,mine,yours)

            return mine, yours

        return f(0, 1)[0]

"""
Runtime: 470 ms, faster than 53.98% of Python3 online submissions for Stone Game II.
Memory Usage: 17.4 MB, less than 28.72% of Python3 online submissions for Stone Game II.

this optimization was not seen
            
            # I can simply take all
            if idx+2*M>=n:
                return summ[-1] - summ[idx]


Runtime: 252 ms, faster than 74.39% of Python3 online submissions for Stone Game II.
Memory Usage: 16.8 MB, less than 32.18% of Python3 online submissions for Stone Game II.

okay...
"""


if __name__ == '__main__':
    s = Solution()
    print(s.stoneGameII(piles=[2, 7, 9, 4, 4]))
    print(s.stoneGameII(piles=[1, 2, 3, 4, 5, 100]))

            

