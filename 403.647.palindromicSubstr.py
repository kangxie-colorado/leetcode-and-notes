"""
https://leetcode.com/problems/palindromic-substrings/

of course I sovled inside-out
but in the DP way

maybe this is like burst ballons... area DP??

f(i,j) {
    if s[i]==s[j], 1+f(i+1,j-1) + f(i+1,j) + f(i,j-1)
    else
        f(i+1,j) + f(i,j-1)
}

let me do this and see if I can convert into bottom up DP
maybe not that easy
"""


from functools import cache


class Solution:
    def countSubstrings(self, s: str) -> int:
        cache = {}

        def isPalindrom(i,j):
            while i<j:
                if s[i]!=s[j]:
                    return False
                i,j=i+1,j-1
            return True

        
        def f(i,j):
            if i>j:
                return 0
            if i==j:
                cache[i,j] = 1
                return 1
            if i==j-1 and s[i]==s[j]:
                cache[i,j] = 3
                return 3
            
            if (i,j) in cache:
                return cache[i,j]
            res = 0
            if s[i] == s[j]:
                # "aBa" split into, "B", "aB" and "Ba".. "B part" should be counted twice
                inner = 1 if isPalindrom(i+1,j-1) else 0
                res += f(i+1, j) + f(i, j-1) - f(i+1, j-1) + inner
            else:
                # "abc" split into "ab" and "bc", the "b part" is counted twice but needed only once
                res += f(i+1, j) + f(i, j-1) - f(i+1,j-1)
        
            cache[i,j] = res
            return res

        print(cache)
        return f(0,len(s)-1)

"""
TLE at 
"dbabcccbcdbbbadabbdabaabcbbabaacdadcdbbbbdddbcbbbcbcabacacdaadaadcdccbacdaadadcbaacabbddabdadcabbccadacadaaacbbddaaababacaabbbacaccbcbbabddbbcccaaacbcdcabcbacdbddcdcadaaadcbccbbcabbcbdaadcbddaacacdadacbbdabcdcdadccaccdbdddddcabdbcdbaadacadadbabdcdbbadaacdbadcdabdbbcabbbdaacaaaaadcaabaaaadabaaddcaabdddcbcadcbdbbdbcbcdbadcadacbbcdccddaccccacbacaacbbdadadcacabdabadbbcdbcaaccdbdcabcadbacbccddbabbdacbcbbcbcabcacdaacccaadcdbdccabcaaacaddadcabacdccaaaddaaadbccdbbcccdddababcdbcddcbdddbbbdaadaccbcaabbcbdbadbabbacdbbbdaaccdcabddacadabcccacdabacbcdbcbdabddacacbdbcaacacaabbaaccddabaadbbaabaddbcacbacdbbbacdccabbcdbbbdbdbbcacabdddbdbaaabbcdcbabcbbbccdcdcdcaaddadccbabbacaddcaddcadcdccaccacabbaababdbbcbdcdccccccdadbdbdcdbdadcdcacdaabaacabaacdacdbaaccadbcddbdccabbcabcadcbdadbcdadbbbccacbcbbcaaaabdacbadacaadcadaacdacddcbbabdacacaabccdaccbbcbbcbcaacdabdcbcdbccdbcbcbddaacdacaaaddcaddcadccacbaddbbbccbbbcbbcbadcabbccbbaadaacacabddbdbddcadbdaaccadbcccabdcdbadbbacbcbbcdcabcddcddddabddbdabdcabdbdbbbcdbcdabbdcb"

but at least I did something differently
"""


class Solution:
    def countSubstrings(self, s: str) -> int:
        @cache
        def isPalindrom(i, j):
            while i < j:
                if s[i] != s[j]:
                    return False
                i, j = i+1, j-1
            return True
        
        # recursive to cover more ground to warm up the cache quicker
        @cache
        def isPalindrom(i, j):
            if i>=j:
                return True
            if s[i]!=s[j]:
                return False
            return isPalindrom(i+1,j-1)
            

        @cache
        def f(i, j):
            if i > j:
                return 0
            if i == j:
                return 1
            if i == j-1 and s[i] == s[j]:
                return 3

            res = 0
            if s[i] == s[j]:
                # "aBa" split into, "B", "aB" and "Ba".. "B part" counted twice... 
                # also the little tricky part is if/only-if inner is palindrom then 1 needs be added
                inner = 1 if isPalindrom(i+1, j-1) else 0
                res += f(i+1, j) + f(i, j-1) - f(i+1, j-1) + inner
            else:
                # "abc" split into "ab" and "bc", the "b part" is counted twice but needed only once
                res += f(i+1, j) + f(i, j-1) - f(i+1, j-1)

            return res

        return f(0, len(s)-1)

"""
used cache for isPalindrom

130 / 130 test cases passed, but took too long.

oka... change to recursive isPalindrome and let cache to warm up quicker
Runtime: 1653 ms, faster than 5.13% of Python3 online submissions for Palindromic Substrings.
Memory Usage: 287.4 MB, less than 5.01% of Python3 online submissions for Palindromic Substrings.

so this is an area DP attempt.. I cannot say solution but only an attempt 
the normal/better solution is to solve each cell.. if it is a palindomic string and if yes, res+=1

can get rid of that special base case for i==j-1
"""


class Solution:
    def countSubstrings(self, s: str) -> int:
        @cache
        def isPalindrom(i, j):
            if i >= j:
                return True
            if s[i] != s[j]:
                return False
            return isPalindrom(i+1, j-1)

        @cache
        def f(i, j):
            if i > j:
                return 0
            if i == j:
                return 1

            res = 0
            if s[i] == s[j]:
                # "aBa" split into, "B", "aB" and "Ba".. "B part" should be counted twice
                inner = 1 if isPalindrom(i+1, j-1) else 0
                res += f(i+1, j) + f(i, j-1) - f(i+1, j-1) + inner
            else:
                # "abc" split into "ab" and "bc", the "b part" is counted twice but needed only once
                res += f(i+1, j) + f(i, j-1) - f(i+1, j-1)

            return res

        return f(0, len(s)-1)

"""
so I think this can be converted to bottom up DP as well
a matrix - "abba"
    a  b  b  a
a   1  2  4  ?  --> 4+4-3+1 = 6(and its right)
b   0  1  3  4
b   0  0  1  2
a   0  0  0  1

dp[i][j] represents s[i:j] inclusive, and the count of palindrome in that substr
rules:
    i>j 0
    i==j 1
so the bottome half will be 0, the diagnoal will be 1

now.. 
dp[i][j] will be 
    if s[i]==s[j]: dp[i-1][j] + dp[i][j-1] - dp[i-1][j+1] + (1 if the whole string(inner) is palindrom or 0)
    else: dp[i-1][j] + dp[i][j-1] - dp[i-1][j+1]

I did a few exampels.. it checks out

so give it a try
notice dp[i][j] depends on i+1,j-1.. so it starts with dp[m-2][n-1] and look to its left and under 

so the scanning is per each diagnol 
"""


class Solution:
    def countSubstrings(self, s: str) -> int:
        @cache
        def isPalindrom(i, j):
            if i >= j:
                return True
            if s[i] != s[j]:
                return False
            return isPalindrom(i+1, j-1)

        n = len(s)
        dp = [[0]*n for _ in range(n)]
        
        # scan per diagnoal
        for diag in range(0, -n, -1):
            for x in range(n):
                y = x - diag
                if y <0 or y>= n:
                    continue
                if x==y:
                    dp[x][y] = 1
                else:
                    self = 0
                    if isPalindrom(x,y):
                        self = 1
                    dp[x][y] = dp[x+1][y] + dp[x][y-1] - dp[x+1][y-1] + self
        
        return dp[0][n-1]

"""
Runtime: 1088 ms, faster than 10.64% of Python3 online submissions for Palindromic Substrings.
Memory Usage: 132 MB, less than 5.63% of Python3 online submissions for Palindromic Substrings.

okay.. still not very efficient.. though I think the time complexity is indeed O(n**2)
that recursive is O(n**2)

let me now do that 
focus on a cell at a time.. 


"""


class Solution:
    def countSubstrings(self, s: str) -> int:
        @cache
        def isPalindrom(i, j):
            if i >= j:
                return True
            if s[i] != s[j]:
                return False
            return isPalindrom(i+1, j-1)

        n = len(s)
        res = 0

        for i in range(n):
            for j in range(i, n):
                if isPalindrom(i,j):
                    res += 1

        return res 

"""
Runtime: 769 ms, faster than 15.41% of Python3 online submissions for Palindromic Substrings.
Memory Usage: 180.6 MB, less than 5.01% of Python3 online submissions for Palindromic Substrings.

convert this to bottom up
notice isPalindrom(i,j) also depends on i+1,j-1

so the same scan 
we can define i>j dp[i][j] = True.. but they don't count --- so we only deal with upper half of the diagnal 

(now I see, my previous attempt is doing some redundant work.. you alread calculated the isPlindrom() on i,j pair...
you can simply run stats on its T/F or 1/0 property.. I then did that aggregation.. anyway fun to try)


"""


class Solution:
    def countSubstrings(self, s: str) -> int:

        n = len(s)
        # init to True but I will explicitly set to false for those not
        # this is just to deal with the lower half easier
        dp = [[1]*n for _ in range(n)]
        res = 0

        for i in range(n-1,-1,-1):
            for j in range(i, n):
                dp[i][j] = 0
                if i==j or (s[i]==s[j] and i+1<n and j-1>=0 and dp[i+1][j-1]):
                    dp[i][j] = 1
                res += dp[i][j]

        return res

"""
Runtime: 335 ms, faster than 41.52% of Python3 online submissions for Palindromic Substrings.
Memory Usage: 22 MB, less than 19.92% of Python3 online submissions for Palindromic Substrings.

overall, the expansion method is the most efficient...
probably because it can end early... 
"""



if __name__ == '__main__':
    s = Solution()
    print(s.countSubstrings("aaa"))
