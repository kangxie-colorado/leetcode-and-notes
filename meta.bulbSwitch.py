"""
a math problem???

n is up to 10**9, not possible to brute force, so observe
f(n) vs f(n-1)

at n-th round, f(n-1) will not be bothered, therefore 
f(n) = f(n-1) + g(n)

g(n)? it turns out to be how many factors it has including 1 and itself
if even number, it will be turned on and off the same times, and it will stay off
if odd number, it will be turned on 1 more time than off, it will stay on
"""

import math


class Solution:
    def bulbSwitch(self, n: int) -> int:
        
        def f(n):
            if n==0: return 0
            if n<=3: return 1

            i = 1
            numFactors = 0
            while i*i < n:
                if n%i==0:
                    numFactors += 2
                i+=1
            if i*i==n:
                numFactors += 1
            
            return f(n-1) + numFactors%2

        return f(n)

"""
TLE...
okay. maybe I can only do bottom up
no.. more observe

it seems if n is a square number it will be on, because it has odd number of factors
1: 1 on
2: 1 2 off
3: 1 3 off
4: 1 2 4, on
5: 1 5 off
6: 1 2 3 6 off
9: 1 3 9 on..

okay 
"""


class Solution:
    def bulbSwitch(self, n: int) -> int:
        
        def f(n):
            if n==0: return 0
            if n<=3: return 1

            sqrt = int(math.sqrt(n))
            return f(n-1) + (sqrt**2 == n)

        return f(n)

""""
okay.. now max recursion depth exceeded
continue to simplify

this is equal to get how many number are sqaure numbers 

"""


class Solution:
    def bulbSwitch(self, n: int) -> int:
        def isSqareNumber(n):
            sqrt = int(math.sqrt(n))
            return sqrt**2 == n
        
        res=0
        for i in range(1,n+1):
            res += isSqareNumber(i)
        
        return res

"""
STIll TLE...
FUCK...

ah.. if I am 9, then 2's square is also here...
why do I need to calculate all one by one
"""            

class Solution:
    def bulbSwitch(self, n: int) -> int:
        return int(math.sqrt(n))
