"""
https://leetcode.com/problems/toss-strange-coins/?envType=study-plan&id=dynamic-programming-ii

DP problem

I have some attempts in the paper and can see two states as well
using an example 

prob = [0.5,0.5,0.5,0.5,0.5]
target = 2

then 
coins can be the column
target can be the rows

    0   1   2   3   4
0
1
2

dp[i][j] => after tossing j-th coin, the probability of i heads 
if i>j+1, dp[i][j] = 0, e.g. dp[2][0]

now dp[i][j]
at j-th coin, two possibilities to form i coins
    1. dp[i][j-1] (at j-1-th coin, already i coins.. thus prob dp[i][j-1]*(1-prob[j])) - not head this time
    2. dp[i-1][j-1], at j-1 coin, only i-1 coins.. and j-th coin is head too... dp[i-1][j-1]*prob[j]
    3. dp[i-2][j-1]... at j-1 coin, only i-2 coin and I do TWO heads.. which is impossible .. 

also, if i-k<0, it is zero naturally
I am thinking maybe I can padding but that makes the semantics hard to understand
okay...


"""


from typing import List


class Solution:
    def probabilityOfHeads(self, prob: List[float], target: int) -> float:
        n = len(prob)
        dp = [[0]*(n+1) for _ in range(target+1)]
        dp[0][0] = 1

        for i in range(len(dp)):
            for j in range(1, n+1):
                if i==0:
                    dp[i][j] = dp[i][j-1] * (1-prob[j-1])
                else:
                    dp[i][j] = dp[i][j-1] * (1-prob[j-1]) + dp[i-1][j-1]*prob[j-1]

        return dp[target][-1]

"""
Runtime: 1458 ms, faster than 63.16% of Python3 online submissions for Toss Strange Coins.
Memory Usage: 51.2 MB, less than 52.63% of Python3 online submissions for Toss Strange Coins.
"""