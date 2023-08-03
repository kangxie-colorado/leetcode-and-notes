"""
https://leetcode.com/problems/shortest-palindrome/?envType=study-plan&id=programming-skills-iii

I am thinking just remove the longest palindrome from the left then the rest is what must be patched?
to test if a string is palindrome.. I can use the bitmap to quickly test out the negative case

for false positive.. I endure the cost
"""


class Solution:
    def shortestPalindrome(self, s: str) -> str:
        bitmap = 0

        for c in s:
            bitmap ^= 1 << (ord(c) - ord('a'))

        def isPalindrome(s, bm):
            lsb = bm & (-bm)
            if bm != lsb:
                return False

            l, r = 0, len(s)-1
            while l < r:
                if s[l] != s[r]:
                    return False
                l, r = l+1, r-1
            return True

        i = len(s)
        while not isPalindrome(s[:i], bitmap):
            i -= 1
            bitmap ^= 1 << (ord(s[i])-ord('a'))

        return s[i:][::-1]+s

"""
Runtime: 66 ms, faster than 85.95% of Python3 online submissions for Shortest Palindrome.
Memory Usage: 14.2 MB, less than 85.25% of Python3 online submissions for Shortest Palindrome.
"""
