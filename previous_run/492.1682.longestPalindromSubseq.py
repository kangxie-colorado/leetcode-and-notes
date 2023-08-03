"""
https://leetcode.com/problems/longest-palindromic-subsequence-ii/

I solved this in O(n^2 * 26) complexity but there is a such solution that is really intriging 

I haven't been able to fully grasp how it works
"""


class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        dp = [0] * len(s)
        for j in range(len(s)):
            inside_max = 0
            for i in range(j - 1, -1, -1):
                if s[j] != s[i]:
                    inside_max = max(inside_max, dp[i])
                else:
                    dp[i] = max(dp[i], inside_max + 2)

                print(i,j,dp[i])
        print(dp)
        return max(dp)

if __name__ == '__main__':
    s = Solution()
    print(s.longestPalindromeSubseq('abcba'))

    print(s.longestPalindromeSubseq('aabaa'))

"""
above examples give

    print(s.longestPalindromeSubseq('abcba'))
0 1 0
1 2 0
0 2 0
2 3 0
1 3 2
0 3 0
3 4 0
2 4 0
1 4 2   <-- dp[1] was set to 2 at line "1 3 2"
0 4 4
[4, 2, 0, 0, 0]
4

so looks like dp[i] represents starting at i, looking rightwards, the longest such subseq's length
it is built up by fixing the right boundary and going left.. 
that makes sense.. fixing right.. expanding towards left...
internal grows when i moves left... and of course i1<i2, i1 would be impacted by i2

the code is really brilliant..
but I haven't been able to understand how it deals with repeating chars.. like below

    print(s.longestPalindromeSubseq('aabaa'))

0 1 2   <-- s[0:1+1] 2
1 2 0   <-- s[1:2+1] 'ab' 0
0 2 2
2 3 0
1 3 2
0 3 2
3 4 2
2 4 0
1 4 2   <-- dp[1] was set to 2 at line "1 3 2" but somehow it doesn't go into internal length.... hmm
            yes, the rightmost char is s[j].. if s[i]!=s[j].. it can go into the internal
            otherwise, it only belong to external layer... 
            hmm... interesting... what kind of relationship this is
            brilliant... but hard to grasp
0 4 2   
[2, 2, 0, 2, 0]
2
"""