"""
https://leetcode.com/problems/4-keys-keyboard/?envType=study-plan&id=dynamic-programming-iii

should be not so hard?
"""


from functools import cache


class Solution:
    def maxA(self, n: int) -> int:
        @cache
        def f(k, screenLen, bufLen, selected):
            if k == 0:
                return screenLen

            res = 0
            res = max(res, f(k-1, screenLen + 1, bufLen, False))  # press 'A'
            if screenLen:
                res = max(res, f(k-1, screenLen, bufLen, True))  # select all
            if selected:
                res = max(res, f(k-1, screenLen, screenLen, False))  # copy
            if bufLen:
                # paste buffer
                res = max(res, f(k-1, screenLen+bufLen, bufLen, False))
            return res

        return f(n, 0, 0, False)

"""
TLE at 37

yeah.. this is 4**n?

maybe select then copy..
it makes no sense to select, then press A or select again..
even copy must be followed by paste.. otherwise, not seeming right either

but that makes thing harder? so keep the paste a step away?
hm.. nah
"""


class Solution:
    def maxA(self, n: int) -> int:
        @cache
        def f(k, screenLen, bufLen):
            if k <= 0:
                return screenLen

            res = 0
            res = max(res, f(k-1, screenLen + 1, bufLen))  # press 'A'
            if screenLen and k>3:
                # select all, then copy and paste
                res = max(res, f(k-3, screenLen*2, screenLen))
            if bufLen:
                # just paste
                res = max(res, f(k-1, screenLen+bufLen, bufLen))

            return res

        return f(n, 0, 0)

"""
okay.. this time I get to 40

can I reduce even one more branch.. 

"""


class Solution:
    def maxA(self, n: int) -> int:
        @cache
        def f(k, screenLen, bufLen):
            if k <= 0:
                return screenLen

            res = 0
            res = max(res, f(k-1, screenLen + max(bufLen, 1), bufLen))  # press 'A' or paste
            if screenLen and k > 3:
                # select all, then copy and paste
                res = max(res, f(k-3, screenLen*2, screenLen))

            return res

        return f(n, 0, 0)

"""
Runtime: 778 ms, faster than 11.86% of Python3 online submissions for 4 Keys Keyboard.
Memory Usage: 140.1 MB, less than 6.78% of Python3 online submissions for 4 Keys Keyboard.

hmm.. there is just a better solution out there I don't know?
math invovled?

not really.. so I am missing something..

okay.. I need to rethink this problem.. 
tomorrow maybe

okay..

dp[k] = max(dp[k-1]+1, dp[k-2]*1, dp[k-3]*2, dp[k-4]*3...)
either press A from last
or select/copy/paste.. 
    k-2, not paste yet; you ask from k-2 and press A, that is actually covered by dp[k-1]
    k-3, can make the copy once
    k-4, can make the copy twice
"""


class Solution:
    def maxA(self, n: int) -> int:

        dp = [0]*(n+1)
        for i in range(1,n+1):
            dp[i] = dp[i-1]+1
            for j in range(2,i):
                dp[i] = max(dp[i], dp[i-j]*(j-1))
        return dp[n]

"""
Runtime: 35 ms, faster than 61.02% of Python3 online submissions for 4 Keys Keyboard.
Memory Usage: 13.8 MB, less than 58.47% of Python3 online submissions for 4 Keys Keyboard.

making one change - also works
"""


class Solution:
    def maxA(self, n: int) -> int:

        dp = [0]*(n+1)
        for i in range(1, n+1):
            dp[i] = dp[i-1]+1
            for j in range(3, i): # start with 3
                dp[i] = max(dp[i], dp[i-j]*(j-1))
        return dp[n]

"""
Runtime: 24 ms, faster than 97.46% of Python3 online submissions for 4 Keys Keyboard.
Memory Usage: 13.9 MB, less than 58.47% of Python3 online submissions for 4 Keys Keyboard.

okay. this solution is pretty good actually - looking forward and reveal that only 3 to 6 is needed
over that.. it can arrive at the same goal from two path.. 
"""

class Solution:
    def maxA(self, n: int) -> int:
        dp = list(range(n + 1))
        for i in range(n - 2):
            for j in range(i + 3, min(n, i + 6) + 1):
                dp[j] = max(dp[j], (j - i - 1) * dp[i])
        return dp[n]

"""
Runtime: 26 ms, faster than 96.61% of Python3 online submissions for 4 Keys Keyboard.
Memory Usage: 13.8 MB, less than 58.47% of Python3 online submissions for 4 Keys Keyboard.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.maxA(3))
    print(s.maxA(7))
