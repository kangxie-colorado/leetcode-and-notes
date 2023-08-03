"""
https://leetcode.com/problems/minimum-ascii-delete-sum-for-two-strings/?envType=study-plan&id=dynamic-programming-ii

seems like another LCS but also biggest LCS.. 
i.e. for a LCS "abc" and "edf".. edf is preferred 

I don't know how to do this efficiently 
but I see a solution -
1. get the dp matrix 
2. retrace back to find all the lcs.. 

s1 = "delete", s2 = "leet"
    " d e l e t e
"   0 0 0 0 0 0 0
l   0 0 0 1 1 1 1
e   0 0 1 1 2 2 2 
e   0 0 1 1 2 2 3 
t   0 0 1 1 2 3 3 

can I reconstruct let from this???
notice it also has "lee" 

actually I can record the lcs along with the number.. 
and maintain the biggest one 

from the diagonal direction. just +1 and append the char
from the horizontal and vertical directions, pick the bigger one 

"""


from collections import Counter


class Solution:
    def minimumDeleteSum(self, s1: str, s2: str) -> int:

        dp = [[ [0,""]]* (len(s2)+1) for _ in range(len(s1)+1)]
        for i in range(1, len(s1)+1):
            for j in range(1, len(s2)+1):
                lcsLen = 0
                lcsStr = ""
                if s1[i-1] == s2[j-1]:
                    lcsLen = dp[i-1][j-1][0] + 1
                    lcsStr = dp[i-1][j-1][1] + s1[i-1]
                else:
                    lcsLen = max(dp[i-1][j][0], dp[i][j-1][0])
                    if dp[i-1][j][0] > dp[i][j-1][0]:
                        lcsStr = dp[i-1][j][1]
                    elif dp[i-1][j][0] < dp[i][j-1][0]:
                        lcsStr = dp[i][j-1][1]
                    else:
                        lcsStr = max(dp[i-1][j][1], dp[i][j-1][1])

                dp[i][j] = [lcsLen, lcsStr]

        print(dp[len(s1)][len(s2)])
        have = Counter(s1+s2)
        keep = Counter( dp[len(s1)][len(s2)][1])

        res = 0
        for char,count in have.items():
            # if char in keep: # no need. counter default to 0
            # print(char, count)
            deletes = count - keep[char]*2
            res += deletes * ord(char)

        return res

"""
there is some errors.. 
I see 
ord(a)=97, ord(z)=122

removing min equals to keeping max 
so 122*ord(a) = 97*ord(z) --- so there can be a choice made somewhere

thus instead of taking biggest 
maybe I convert it to ascii values accumulations already 

give a try
"""


class Solution:
    def minimumDeleteSum(self, s1: str, s2: str) -> int:

        dp = [[[0, 0]] * (len(s2)+1) for _ in range(len(s1)+1)]
        for i in range(1, len(s1)+1):
            for j in range(1, len(s2)+1):
                lcsLen = 0
                lcsAscii = 0
                if s1[i-1] == s2[j-1]:
                    lcsLen = dp[i-1][j-1][0] + 1
                    # this adds one more char so it has to grow
                    lcsAscii = dp[i-1][j-1][1] + ord(s1[i-1])
                else:
                    lcsLen = max(dp[i-1][j][0], dp[i][j-1][0])
                    lcsAscii = max(dp[i-1][j][1], dp[i][j-1][1])

                dp[i][j] = [lcsLen, lcsAscii]

        print(dp[len(s1)][len(s2)])

        totalAsciiVal = 0
        for c in s1+s2:
            totalAsciiVal += ord(c)

        return totalAsciiVal - dp[len(s1)][len(s2)][1]*2

"""
Runtime: 1093 ms, faster than 66.59% of Python3 online submissions for Minimum ASCII Delete Sum for Two Strings.
Memory Usage: 24.5 MB, less than 35.05% of Python3 online submissions for Minimum ASCII Delete Sum for Two Strings.

this is right too -- making no assumption that diagonal is always the best
"""


class Solution:
    def minimumDeleteSum(self, s1: str, s2: str) -> int:

        dp = [[[0, 0]] * (len(s2)+1) for _ in range(len(s1)+1)]
        for i in range(1, len(s1)+1):
            for j in range(1, len(s2)+1):
                lcsLen = 0
                lcsAscii = 0
                if s1[i-1] == s2[j-1]:
                    lcsLen = dp[i-1][j-1][0] + 1
                    lcsAscii = dp[i-1][j-1][1] + ord(s1[i-1])

                lcsLen = max(lcsLen, dp[i-1][j][0], dp[i][j-1][0])
                lcsAscii = max(lcsAscii, dp[i-1][j][1], dp[i][j-1][1])

                dp[i][j] = [lcsLen, lcsAscii]

        # print(dp[len(s1)][len(s2)])

        totalAsciiVal = 0
        for c in s1+s2:
            totalAsciiVal += ord(c)

        return totalAsciiVal - dp[len(s1)][len(s2)][1]*2


"""
Runtime: 1179 ms, faster than 64.72% of Python3 online submissions for Minimum ASCII Delete Sum for Two Strings.
Memory Usage: 24.6 MB, less than 35.05% of Python3 online submissions for Minimum ASCII Delete Sum for Two Strings.
"""

if __name__ == '__main__':
    s = Solution()
    # print(s.minimumDeleteSum("sea", "eat"))
    # print(s.minimumDeleteSum("delete", "leet"))

    s1 = "igijekdtywibepwonjbwykkqmrgmtybwhwjiqudxmnniskqjfbkpcxukrablqmwjndlhblxflgehddrvwfacarwkcpmcfqnajqfxyqwiugztocqzuikamtvmbjrypfqvzqiwooewpzcpwhdejmuahqtukistxgfafrymoaodtluaexucnndlnpeszdfsvfofdylcicrrevjggasrgdhwdgjwcchyanodmzmuqeupnpnsmdkcfszznklqjhjqaboikughrnxxggbfyjriuvdsusvmhiaszicfa"
    s2 = "ikhuivqorirphlzqgcruwirpewbjgrjtugwpnkbrdfufjsmgzzjespzdcdjcoioaqybciofdzbdieegetnogoibbwfielwungehetanktjqjrddkrnsxvdmehaeyrpzxrxkhlepdgpwhgpnaatkzbxbnopecfkxoekcdntjyrmmvppcxcgquhomcsltiqzqzmkloomvfayxhawlyqxnsbyskjtzxiyrsaobbnjpgzmetpqvscyycutdkpjpzfokvi"
    print(s.minimumDeleteSum(s1, s2))


    s1 = "igijekdtywibepwonjbwykkqmrgmtybwhwjiqpcxukrablqmwjndlhblxflg"
    s2 = "ikhuivqoriaqybciofdzbdie"
    s3 = "ikhuivqoriwbjaqybciofdzbdie"
    # help debugging s1 vs s3 wrong answer
    # s1 vs s2. right 
    print(s.minimumDeleteSum(s1, s2))
    print(s.minimumDeleteSum(s1, s3))
