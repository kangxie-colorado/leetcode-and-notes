"""
https://leetcode.com/problems/word-break/?envType=study-plan&id=dynamic-programming-ii

kind of forgot how to do this but recursive not hard to see

f(i) - represents if s[i:] can be broken into words
    for each word in words:
        if s[i:i+l] == word and f(i+l):
            return True
    return False
"""


from functools import cache
from typing import List


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        @cache
        def f(i):
            if i == len(s):
                return True
        
            for word in wordDict:
                if s[i:i+len(word)] == word and f(i+len(word)):
                    return True
            return False
        return f(0)
"""
Runtime: 31 ms, faster than 97.47% of Python3 online submissions for Word Break.
Memory Usage: 14.1 MB, less than 26.77% of Python3 online submissions for Word Break.
(with cache)

okay.. let me see the bottom up... 

if I use a one dimension dp, (the f() has only one argument, so kind of it is 1-D)
dp[i] --  represent upto i, can it be broken or not
    dp[0] = True (this is left padding)
    dp[i] = {
        for word in words:
            if i>=len(word):
                dp[i] != dp[i-len(word)]
    }

a bit unnatural.. let me see
"""


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        dp = [0]*(len(s)+1)

        dp[0] = 1
        for i in range(1,len(s)+1):
            for word in wordDict:
                if i>=len(word):
                    dp[i] |= dp[i-len(word)]
        return dp[len(s)]

"""
ahah... 
                if i>=len(word):
                    dp[i] |= dp[i-len(word)]
        
        I thought of something so simple then got kicked 

        you have to match both end 
        or at least match this ending part because you can take to dp |= ...

"""


class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        dp = [0]*(len(s)+1)

        dp[0] = 1
        for i in range(1, len(s)+1):
            for word in wordDict:
                if i >= len(word) and word == s[i-len(word):i]:
                    dp[i] |= dp[i-len(word)]
                # could use this to terminate the inner loop earlier
                if dp[i]:
                    break
        return dp[len(s)]

"""
Runtime: 44 ms, faster than 67.26% of Python3 online submissions for Word Break.
Memory Usage: 13.8 MB, less than 93.66% of Python3 online submissions for Word Break.

Runtime: 34 ms, faster than 94.26% of Python3 online submissions for Word Break.
Memory Usage: 13.8 MB, less than 99.78% of Python3 online submissions for Word Break.
with early termination 
"""