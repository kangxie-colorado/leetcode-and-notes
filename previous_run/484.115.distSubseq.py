"""
https://leetcode.com/problems/distinct-subsequences/?envType=study-plan&id=dynamic-programming-iii


okay.. it seems like totally no idea
but if going back to one char at a time.. maybe the algorithm is like this

f(i,j): represents how many subsequence there is 

    if s[i] != t[j]: 
        then i has to move forward
    if s[i] == t[j]: 
        there is a choice to make and the total should be the sum up of following
        f(i+1,j+1) # taking this pair
        f(i+1,j) # chances are there are more same characters to the back so try later

    if j reaches len(t): then this is one
    if i reaches len(s): then this is zero

seems it might work

"""


from functools import cache


class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        @cache
        def f(i,j):
            if j == len(t):
                return 1
            if i==len(s):
                return 0

            if s[i]!=t[j]:
                return f(i+1,j)
            
            return f(i+1,j+1) + f(i+1,j)
        
        return f(0,0)

"""
Runtime: 703 ms, faster than 45.01% of Python3 online submissions for Distinct Subsequences.
Memory Usage: 156.8 MB, less than 12.83% of Python3 online submissions for Distinct Subsequences.

okay.. leave the bottom up to future exercise 

"""

if __name__ == '__main__':
    sol = Solution()
    print(sol.numDistinct(s="rabbbit", t="rabbit"))

    print(sol.numDistinct(s="babgbag", t="bag"))
    s = "daacaedaceacabbaabdccdaaeaebacddadcaeaacadbceaecddecdeedcebcdacdaebccdeebcbdeaccabcecbeeaadbccbaeccbbdaeadecabbbedceaddcdeabbcdaeadcddedddcececbeeabcbecaeadddeddccbdbcdcbceabcacddbbcedebbcaccac"
    t="ceadbaa"
    print(sol.numDistinct(s,t))
