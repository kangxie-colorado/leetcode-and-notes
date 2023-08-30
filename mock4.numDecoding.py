from functools import cache


class Solution:
    def numDecodings(self, s: str) -> int:
        
        @cache
        def f(idx):
            if idx==len(s):
                return 1
            
            if s[idx] == "0" or (idx+1<len(s) and s[idx+1]=="0" and s[idx]>"2"):
                return 0
            
            res = f(idx+1)
            if idx+1 < len(s):
                if "10"<=s[idx:idx+2]<="26":
                    res += f(idx+2)
            
            return res
        return f(0)

if __name__ == '__main__':
    s = Solution()
    print(s.numDecodings("12"))
    print(s.numDecodings("226"))
    print(s.numDecodings("227"))
    print(s.numDecodings("06"))
                