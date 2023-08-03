"""
https://leetcode.com/problems/shortest-way-to-form-string/

did this 2 months ago but don't remember not a lot..

thinking keep an idx i for source, when it walks over boundary.. start a new seq 

and just need to go thru target 1 by 1... to see where it goes
let me see 

let me eat first
"""


class Solution:
    def shortestWay(self, source: str, target: str) -> int:
        if not set(target).issubset(set(source)):
            return -1

        count = 1
        def f(sIdx, tIdx):
            nonlocal count
            if tIdx >= len(target):
                return count
            
            if sIdx >= len(source):
                
                count += 1
                sIdx = 0
            
            if source[sIdx] == target[tIdx]:
                return f(sIdx+1, tIdx+1)
            else:
                return f(sIdx+1, tIdx)
        
        return f(0,0)

"""
Runtime: 118 ms, faster than 28.38% of Python3 online submissions for Shortest Way to Form String.
Memory Usage: 42.4 MB, less than 6.39% of Python3 online submissions for Shortest Way to Form String.

okay.. when mind is rested and clear.. it does help solve problems quicker?!
let me see bottom up or iterative
"""


class Solution:
    def shortestWay(self, source: str, target: str) -> int:
        if not set(target).issubset(set(source)):
            return -1
        count = 1
    
        sIdx = tIdx = lastTIdx = 0
        while tIdx < len(target):

            if sIdx == len(source):
                count += 1
                sIdx = 0
                if tIdx == lastTIdx:
                    return -1
            
            if source[sIdx] == target[tIdx]:
                sIdx += 1
                tIdx += 1
            else:
                sIdx += 1
        return count

"""
Runtime: 76 ms, faster than 51.47% of Python3 online submissions for Shortest Way to Form String.
Memory Usage: 13.8 MB, less than 79.73% of Python3 online submissions for Shortest Way to Form String.
"""


class Solution:
    def shortestWay(self, source: str, target: str) -> int:
        count = 1

        sIdx = tIdx = lastCountStartIdx = 0
        while tIdx < len(target):

            if sIdx == len(source):
                count += 1
                sIdx = 0

                if tIdx == lastCountStartIdx:
                    return -1
                lastCountStartIdx = tIdx

            if source[sIdx] == target[tIdx]:
                sIdx += 1
                tIdx += 1
            else:
                sIdx += 1
        return count

"""
Runtime: 60 ms, faster than 70.02% of Python3 online submissions for Shortest Way to Form String.
Memory Usage: 13.9 MB, less than 79.73% of Python3 online submissions for Shortest Way to Form String.

still where is the DP

dp[j]: represent at idx-j of target, the state, what is the state?
    (i, count): the index of source and how many has been used?
    but then you can see it only depends on the left element so a variable is enough 
    I wonder do I miss anything if I stop digging deeper here.. 


okay.. review my previous submissions.. it seems this time I did better?
s-macbook-pro:leetcode-and-notes xiekang$ ls -rlt * | grep 1055
-rw-r--r--  1 xiekang  staff      800 Nov 25 10:42 294.1055.shortestToFormStr.py
-rw-r--r--  1 xiekang  staff     3167 Jan 16 16:12 406.1055.shortestWays.py

so I have improved in 2 months??
"""
        
if __name__ == '__main__':
    s = Solution()
    print(s.shortestWay(source="abc", target="abcbc"))
