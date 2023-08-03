""""
https://leetcode.com/problems/longest-palindromic-subsequence/
the acceptance ratio is high, but I don't see the solution really quick
hmm.. let me think 

if A is a such subseq, xAx will be too 
    A can start odd, a single char
    A can start even, two same chars.. 

if I define f(i,j) to represent from i to j, inclusive, the longest palindrom 

what is the relationship for f(i,j) vs its interval state?
    if s[i] == s[j], f(i,j) = f(i+1,j-1) + 2
    else: max(f(i+1,j), f(i,j-1))

    bases:
        i>j, 0 and ""
        i==j, 1 and s[i]
        i==j-1, this can be covered by first base

is that right?
worthy a try 

"""


from functools import cache


class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:

        @cache
        def f(i, j):
            if i > j:
                return 0, ""
            if i == j:
                return 1, s[i]

            pLen, pStr = 0, ""
            if s[i] == s[j]:
                spLen, spStr = f(i+1, j-1)
                pLen, pStr = 2+spLen, s[i]+spStr+s[i]
            else:
                lpLen, lpStr = f(i, j-1)
                rpLen, rpStr = f(i+1, j)
                pLen, pStr = lpLen, lpStr
                if lpLen < rpLen:
                    pLen, pStr = rpLen, rpStr
            return pLen, pStr
        return f(0, len(s)-1)[0]


class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:

        @cache
        def f(i, j):
            if i > j:
                return 0
            if i == j:
                return 1

            if s[i] == s[j]:
                return 2+f(i+1, j-1)
            else:
                return max(f(i+1, j), f(i, j-1))
        return f(0, len(s)-1)

"""
Runtime: 1006 ms, faster than 92.60% of Python3 online submissions for Longest Palindromic Subsequence.
Memory Usage: 251.1 MB, less than 6.89% of Python3 online submissions for Longest Palindromic Subsequence.

very obviously, this can be solved in the diagnaol dp
or actually no need to scan diagnoally but to start at the diagnol position
"""


class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        n = len(s)
        dp = [[0]*n for _ in range(n)]
        for i in range(n-1,-1,-1):
            for j in range(i,n):
                
                if i==j:
                    dp[i][j] = 1
                else:
                    if s[i] == s[j]:
                        dp[i][j] = 2+dp[i+1][j-1]
                    else:
                        dp[i][j] = max(dp[i+1][j], dp[i][j-1])

        return dp[0][n-1]

"""
Runtime: 1431 ms, faster than 78.73% of Python3 online submissions for Longest Palindromic Subsequence.
Memory Usage: 30.6 MB, less than 74.24% of Python3 online submissions for Longest Palindromic Subsequence.
"""