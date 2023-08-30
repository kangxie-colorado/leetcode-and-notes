"""
n can be big, s is small
so the focus should be s

just trim off s

0 1 -> 1 len
10 11 -> 2
100 101 110 111 -> 3
"""

class Solution:
    def queryString(self, s: str, n: int) -> bool:
        lastN = 0
        i = 0
        binS = bin(lastN)[2:]
        while i<len(s) and s[i:i+len(binS)] == binS:
            i += len(binS)
            lastN += 1
            binS = bin(lastN)[2:]
        
        return lastN >= n

"""
okay.. damn.. it is not like what I understand
it can be any substr
"""