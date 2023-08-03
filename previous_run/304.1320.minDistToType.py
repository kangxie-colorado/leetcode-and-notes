"""
https://leetcode.com/problems/minimum-distance-to-type-a-word-using-two-fingers/

I watched the solution and now trying to reproduce it

"""


class Solution:
    def minimumDistance(self, word: str) -> int:

        def cost(c1, c2):
            # first typing
            if c1 == 26:
                return 0

            return abs(c1//6 - c2//6) + abs(c1 % 6 - c2 % 6)

        cache = {}

        def f(i, otherFinger):
            # i: the idx the typing has proceded to
            # otherFig: the char the other finger is on (represented by the ord(Char)- ord('A))
            if i == len(word)-1:
                return 0

            if (i, otherFinger) in cache:
                return cache[(i, otherFinger)]

            # this finger continues to type vs other finger to type (thus this finger becomes other finger)
            cache[(i, otherFinger)] = min(f(i+1, otherFinger) + cost(ord(word[i]) - ord('A'), ord(word[i+1])-ord('A')),
                                          f(i+1, ord(word[i]) - ord('A')) + cost(otherFinger, ord(word[i+1])-ord('A')))
            return cache[(i, otherFinger)]

        return f(0, 26)


""""
Runtime: 545 ms, faster than 75.00% of Python3 online submissions for Minimum Distance to Type a Word Using Two Fingers.
Memory Usage: 18.8 MB, less than 54.07% of Python3 online submissions for Minimum Distance to Type a Word Using Two Fingers.
"""
