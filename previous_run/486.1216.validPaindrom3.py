"""
https://leetcode.com/problems/valid-palindrome-iii/?envType=study-plan&id=dynamic-programming-iii

high ac ratio: if you find the pattern, it ought to be not so hard

I have no idea.. but I am thinking for palindrom.. of course I can start with begin/end.. two pointer

f(i,j,k)
    if s[i]==s[j]:
        the char can stay.. 
        f(i+1,j-1,k)
    else:
        # I can remove s[i]
        f(i+1,j,k-1)
        or 
        # I can remove s[j]
        f(i,j-1,k-1)

        then either of them being true.. it is true
    
    bases:
        i==j:
            return True
        i==j-1:
            if k>0
                return True
            else:
                return False
        k==0?
            return is the string palinDrom

give a try
            
"""


from functools import cache


class Solution:
    def isValidPalindrome(self, s: str, k: int) -> bool:
        
        @cache
        def f(i,j,k):
            if k==0:
                ii,jj=i,j
                while ii<jj:
                    if s[ii] != s[jj]:
                        return False
                    ii,jj=ii+1,jj-1
                return True

            if i==j:
                return True
            if i==j-1:
                return k>0
            
            if s[i] == s[j]:
                return f(i+1,j-1,k)
            
            return f(i+1,j,k-1) or f(i,j-1,k-1)

        return f(0,len(s)-1,k)

"""
Runtime: 1424 ms, faster than 16.73% of Python3 online submissions for Valid Palindrome III.
Memory Usage: 281.9 MB, less than 10.18% of Python3 online submissions for Valid Palindrome III.

"""

if __name__ == '__main__':
    sol = Solution()
    print(sol.isValidPalindrome(s="abcdeca", k=2))
    print(sol.isValidPalindrome(s="abbababa", k=2))
    print(sol.isValidPalindrome(s="abbababa", k=0))
    s = "fcgihcgeadfehgiabegbiahbeadbiafgcfchbcacedbificicihibaeehbffeidiaiighceegbfdggggcfaiibefbgeegbcgeadcfdfegfghebcfceiabiagehhibiheddbcgdebdcfegaiahibcfhheggbheebfdahgcfcahafecfehgcgdabbghddeadecidicchfgicbdbecibddfcgbiadiffcifiggigdeedbiiihfgehhdegcaffaggiidiifgfigfiaiicadceefbhicfhbcachacaeiefdcchegfbifhaeafdehicfgbecahidgdagigbhiffhcccdhfdbd"
    k=216
    print(sol.isValidPalindrome(s,k))
