"""
https://leetcode.com/problems/longest-palindromic-substring/

still O(n**2)
expansion or dp

dp I save the length -- and I use len == j-i+1 to mean if it is palindrom implicitly
I can init the len to 0 

for those i==j+1, j-i+1 is the total length -> j-(j+1)+1 = 0
seems so coincidental.. 


"""


class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        dp = [[0]*n for _ in range(n)]
        maxLen, maxStr = 0,""

        for i in range(n-1, -1, -1):
            for j in range(i, n):
                if i==j or (dp[i+1][j-1] == j-1 - (i+1) + 1 and s[i]==s[j]):
                    # dp[i+1][j-1] == j-1 - (i+1) + 1: that means at i+1,j-1 it is palindrom
                    # for i+1>j-1 cases, it is naturally included
                    #   this targets the diagonal line beline the left/up -> right/bottom line
                    #   further downwards lines are not needed for consideration 
                    dp[i][j] = j-i+1

                if dp[i][j] > maxLen:
                    maxLen = dp[i][j]
                    maxStr = s[i:j+1]

        return maxStr


"""
Runtime: 6365 ms, faster than 13.39% of Python3 online submissions for Longest Palindromic Substring.
Memory Usage: 30.5 MB, less than 5.26% of Python3 online submissions for Longest Palindromic Substring.

cool... min code at least... 
"""