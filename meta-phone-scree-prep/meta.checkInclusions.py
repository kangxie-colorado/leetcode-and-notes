"""
because it is substring so it has to be continuous 
so the length is fixed to s1.len()


"""

from collections import Counter


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False
      
        c1 = Counter(s1)
        c2 = Counter(s2[:len(s1)])
        for i in range(len(s1), len(s2)):
            if c1 == c2:
                return True
            
            leavingChar = s2[i-len(s1)]
            c2[leavingChar] -= 1
            if c2[leavingChar] == 0:
                c2.pop(leavingChar)
            
            enteringChar = s2[i]
            c2[enteringChar] += 1
        
        return c1 == c2

if __name__ == '__main__':
    s = Solution()
    print(s.checkInclusion(s1 = "adc", s2 = "dcda"))