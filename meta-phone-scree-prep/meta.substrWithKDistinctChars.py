"""
this should be a sliding window

didn't see what is in the string but could assume it is ascii but do I need it?

"""

from collections import defaultdict


class Solution:
    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        charsInWindow = defaultdict(int)
        def distinctChars():
            return len(charsInWindow)

        i=j=0
        res=0
        while j<len(s):
            charsInWindow[s[j]] += 1

            # if it doesn't meet, sliding i
            while distinctChars() > k:
                charsInWindow[s[i]] -= 1
                if charsInWindow[s[i]] == 0:
                    charsInWindow.pop(s[i])
                i+=1 
            
            # now this window is legit
            res = max(res, j-i+1)
            j+=1
        
        return res
    
if __name__ == '__main__':
    s = Solution()
    print(s.lengthOfLongestSubstringKDistinct(s = "eceba", k = 2))