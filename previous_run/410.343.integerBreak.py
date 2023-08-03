"""
https://leetcode.com/problems/integer-break/

ah.. interesting

f(n) = max [
    f(n-1)*1, (n-1)*1
    f(n-2)*2, (n-2)*2
    f(n-3)*3
    f(n-4)*4
    ...
    f(2)*(n-1)
]


"""


from functools import cache


class Solution:
    def integerBreak(self, n: int) -> int:

        @cache
        def f(i):
            if i<=2:
                return 1

            res = 0
            for j in range(1,i):
                res = max(res, f(j)*(i-j), j*(i-j))
            return res
        return f(n)

"""
Runtime: 36 ms, faster than 78.69% of Python3 online submissions for Integer Break.
Memory Usage: 13.9 MB, less than 17.39% of Python3 online submissions for Integer Break.

let me see bottome up
"""


class Solution:
    def integerBreak(self, n: int) -> int:
        dp = [1] * (n+1)

        for i in range(3, n+1):
            for j in range(1, i):
                dp[i] = max(dp[i], dp[i-j]*j, (i-j)*j)

        return dp[n]

if __name__ == '__main__':
    print(Solution().integerBreak(10))