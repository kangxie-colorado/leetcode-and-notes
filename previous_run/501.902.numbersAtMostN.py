"""
https://leetcode.com/problems/numbers-at-most-n-given-digit-set/?envType=study-plan&id=dynamic-programming-iii

not quite sure how to go about this?
use any digit as first.. then 2nd?..
"""


from typing import List


class Solution:
    def atMostNGivenDigitSet(self, digits: List[str], n: int) -> int:
        
        def f(run):
            if run and int(run) > n:
                return 0
            

            res = 1
            for d in digits:
                res += f(run+d)
            
            return res

        return f("")-1

"""
okay.. this has to TLE
I admit I cannot figure this out myself

so looked at others.. what happens is case study

1. all the numbers with less digits will of course meet
    and it will be like len(digits)**i for i in range(1,n)
    because in every number, each digit has len(D) choices
    hence D**i for i in range(1,n)

2. then all the number with more digits, of course cannot so don't care
3. then all the number with same digits..
    how to go about this?
    - if the first digit is smaller, then that left n-1 digits to be free for all
    e.g. n=338, 1** 2** would be free for all, that means D**2 (n-i-1)
    - then the next batch to check is 3**
        that needs 3 to be in the digit set, because if 3 is not, then 2**,1** are counted already; 4**.. are not useful
        so 3 has to be in there.. otherwise we end
    - lets say the 3 is there.. this becomes a recursive definition 
        31*, 32*..
        to do this.. we compare the digits in set to be smaller than the corresponding digit in str to see how many can be this at this pos
    ... 
4. it will miss an edge case.. 
    that is everything is equal.. 
        

"""


class Solution:
    def atMostNGivenDigitSet(self, digits: List[str], n: int) -> int:
        nStr = str(n)
        nLen = len(nStr)

        res = sum(len(digits)**i for i in range(1,nLen))
        i=0
        while i<nLen:
            res += sum(d < nStr[i] for d in digits) * (len(digits)**(nLen-1-i))
            if nStr[i] not in digits:
                break
            i+=1
        
        return res + (i==nLen)

"""
Runtime: 24 ms, faster than 97.50% of Python3 online submissions for Numbers At Most N Given Digit Set.
Memory Usage: 13.8 MB, less than 98.33% of Python3 online submissions for Numbers At Most N Given Digit Set.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.atMostNGivenDigitSet(digits = ["1","3","5","7"], n = 100))
    print(s.atMostNGivenDigitSet(digits = ["1","4","9"], n = 1000000000))