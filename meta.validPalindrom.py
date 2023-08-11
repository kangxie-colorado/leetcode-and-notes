from functools import cache


class Solution:
    def validPalindrome(self, s: str) -> bool:
        @cache
        def f(i,j,left):
            if i>=j:
                return True
            
            if s[i]==s[j]:
                return f(i+1,j-1, left)
            
            if left:
                return f(i,j-1,0) or f(i+1,j,0)
            return False
        
        return f(0,len(s)-1,1)