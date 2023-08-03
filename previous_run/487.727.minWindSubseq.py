"""
https://leetcode.com/problems/minimum-window-subsequence/

not sure it will work but this is what I thought

for each char, records its positions
Input: s1 = "abcdebdde", s2 = "bde"

{
    'a': [0]
    'b': [1,5]
    'c': [2]
    'd': [3,6,7]
    'e': [4,8]
}

then I have to match s2 
one by one

'b': 1, pop it out 
search in 'd' the first > 1: 3, pop it out and here I shall record 3 as window lenght (3) but can use 2 (3-1) to simplify
search in 'e' the first > 4: 4, pop it out and update the window length, increment it by 1 => 3 (which means 4)

then this is a candidate!

then b:5... 

probably will not work.. just give a try and go watch tv



"""


import bisect
from collections import defaultdict, deque


class Solution:
    def minWindow(self, s1: str, s2: str) -> str:
        charPostions = defaultdict(list) 
        for i,c in enumerate(s1):
            charPostions[c].append(i)

        resLen = float('inf')
        res= ""
        initPosIdx = 0
        while initPosIdx < len(charPostions[s2[0]]):
            pos = charPostions[s2[0]][initPosIdx]
            wind = []
            for c in s2:
                if c not in charPostions:
                    return ""
                
                posIdx = bisect.bisect_left(charPostions[c], pos)
                if posIdx >= len(charPostions[c]):
                    return res
                wind.append(charPostions[c][posIdx])
                # it will be at least +1 to get next char
                # so +1 is safe and a trick to avoid duplciates (see below example 1)
                # +1 will make sure the next search get to next 'm'
                pos = charPostions[c][posIdx] + 1
                charPostions[c] = charPostions[c][posIdx:]
   
            if len(wind)==len(s2) and wind[-1]-wind[0]+1 < resLen:
                resLen = wind[-1]-wind[0]+1
                res = s1[wind[0]:wind[-1]+1]
            
            initPosIdx+=1
        return res

"""
Runtime: 361 ms, faster than 40.06% of Python3 online submissions for Minimum Window Subsequence.
Memory Usage: 15.1 MB, less than 35.91% of Python3 online submissions for Minimum Window Subsequence.

woow..
"""

if __name__ == '__main__':
    s = Solution()
    print(s.minWindow("cnhczmccqouqadqtmjjzl", "mm"))
    print(s.minWindow("wcbsuiyzacfgrqsqsnodwmxzkz", "xwqe"))
    print(s.minWindow(s1="abcabcdbebdbabcbeddebdde", s2="bde"))
    print(s.minWindow(s1="jmeqksfrsdcmsiwvaovztaqenprpvnbstl", s2="u"))


        



            



                