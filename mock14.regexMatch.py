from functools import cache


class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        
        @cache
        def f(i,j):
            if i==len(s):
              if j==len(p) or (j==len(p)-1 and p[j]=='*') or(j==len(p)-2 and p[j+1]=='*'):
                return True
              return False
            
            if j==len(p):
                return False
                          
            if p[j] == '*':
                # no more repeating
                res = f(i,j+1)
                # more repeating
                if s[i]==p[j-1] or p[j-1]=='.':
                    res |= f(i+1,j) 
                return res
            
            if s[i] != p[j] and p[j]!='.':
              if (j+1)>=len(p) or p[j+1]!="*": # * as zero
                  return False
              else:
                  return f(i,j+2)
            else:
                  return f(i+1,j+1)

        return f(0,0)



class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        
        @cache
        def f(i,j):
            if i==len(s) and j==len(p):
                return True
              
            if j==len(p):
                return False

            if i<len(s):   
              if j+1<len(p) and p[j+1] == '*':
                  return f(i,j+2) or ((s[i] == p[j] or p[j] == '.') and f(i+1,j))
              else:
                  return (s[i] == p[j] or p[j] == '.' ) and f(i+1,j+1)

            # let all the .* a* b* be skipped when s is used up
            return (j+1<len(p) and p[j+1] == '*' and f(i,j+2)) or False
        return f(0,0)

if __name__ == '__main__':
    s = Solution()
    # print(s.isMatch(s = "aa", p = "a"))
    print(s.isMatch(s = "aa", p = "a*"))
    print(s.isMatch(s = "aa", p = "a*c"))
    print(s.isMatch(s = "aa", p = "a*a"))
    print(s.isMatch(s = "aab", p = "c*a*b"))
    print(s.isMatch(s = "ab", p = ".*c"))

                
                