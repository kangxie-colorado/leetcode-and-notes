"""
https://leetcode.com/problems/factor-combinations/

interesting...
so I guess first I need to compute its all factors first? 
top-down??? and backtrack.. but could use the same number more than one time

kind of like coin change
but there are other nuances..

so how about I break it down to prim factors.. 
12, to [2,2,3] 
then I can combine first 2, second 2 
it could go like sorted 3-sum... on next loop I skip those used numbers. 


not sure if it could work.. 
at least interesting to try
"""


from functools import cache
import math
from typing import List
import sympy 

class Solution:
    def getFactors(self, n: int) -> List[List[int]]:
        def isPrime(num):
            if num<=3:
                return True
            for f in range(2, int(math.sqrt(num))+1):
                if num%f == 0:
                    return False
            return True

        @cache
        def getPrimeFactors(num):    
            if num==1 or sympy.isprime(num):
                return [num]

            res = []
            for i in range(2, int(math.sqrt(num))+1):
                if num%i==0:
                    res.extend(getPrimeFactors(i))
                    res.extend(getPrimeFactors(num//i))
                    break
            return res 

        primeFactors = getPrimeFactors(n)
        if primeFactors[-1] == n:
            primeFactors.pop()
        
        res = [primeFactors]

        for i in range(len(res)-1):
            ...

        # okay I realize this is not gonna work
        # because after any 2 can combine.. any 3 can combine too
        # any 4/5/6.. and it will quickly overlap..
        # I think I might be able to make it work.. but let me think the other way

        return None


"""
if I break down 12 to factors as such [2,3,4,6]

then I use a dp
dp[i] represent the combinations of i's factor can be broken down

dp[1] = [[]] # nested list to start.. but it needs to return None
dp[prime_num] = [[prime_num]] # prime_num itself.  

dp[i] = {
    for f in factors:
        if i%f==0:
            nest dp[f] and dp[i//f] together
            e.g. dp[2] = [[2]], dp[[3]] == [[3]] so for dp[6] it will be [[2,3]]
                e.g. for dp[8], it will be dp[2] vs dp[4], then dp[4] vs dp[2]??????
                so maybe I need to scan factor in the outer loop and scan i in the inner loop?????
}

give a try, whatever

"""


class Solution:
    def getFactors(self, n: int) -> List[List[int]]:
        def getPrimeFactors(num):
            res = []
            for i in range(2, int(math.sqrt(num))+1):
                if num%i==0:
                    res.append(i)
                    res.append(num//i)
            return res 
        
        dp = [None for _ in range(n+1)]
        factors = getPrimeFactors(n)
        print(factors)

        for f in factors:
            for i in range(2,n+1):
                if sympy.isprime(i):
                    dp[i] = [[i]]
                else:
                    ...
        # hum... 12 is broken to [2,6,3,4] I cannot even see 2,2,3 possibility 
        # so this route cannot pass possibily I should go back to above 
        return None

"""
so okay.. 
I have broken 12 to [2,2,3]

now I want to run some code to get [2,6] and [3,4]
it can multiply 

if I say 
using the first num to combine laters I have two choice at each number 
I can choose or not choose, right

2,2,3
at first 2
    on 2nd 2, 
        - I choose not to combine, [2,2]
            when idx is left with only one, can I combine?
                [2,2,3] not to combine
                [2,6] is to combine with prod (maybe should be 6,2)
        - I choose to combin [4]
            now facing [3], there are only only left, and only one in the run.. cannot combine - so [4,3]

then I skip all the equal values 
    I go to 3.. [2,2]
        I get [2,2,3]???

hmm? ... still hard to break
I see the similar question is combination sum.. 
which is to keep the possibilities around.

let me go back to that again??????
hmm...

2,2,3
first it is [2]
then 2 can be [4] [2,2]
then 3 can be [4,3] [2,2,3] [2,6] [6,2]???


"""


class Solution:
    def getFactors(self, n: int) -> List[List[int]]:
        @cache
        def getPrimeFactors(num):
            if num == 1 or sympy.isprime(num):
                return [num]

            res = []
            for i in range(2, int(math.sqrt(num))+1):
                if num % i == 0:
                    res.extend(getPrimeFactors(i))
                    res.extend(getPrimeFactors(num//i))
                    break
            return res

        primeFactors = getPrimeFactors(n)
        if primeFactors[-1] == n:
            primeFactors.pop()
        
        if not primeFactors:
            return None

        # now I walk the primeFactors 
        # for each previously partitial results 
        # I combine and push back 
        run = [[primeFactors[0]]]
        for pf in primeFactors[1:]:
            # it can be appended to temp 
            # it can also be applied as a prod to temp 
            # but here you need to skip duplicates 
            tmp = []
            for pRun in run:
                # this is simply append 
                tmp.append(sorted(pRun + [pf]))
                
                prods = [i*pf for i in pRun]
                usedProds = set()
                for i,prod in enumerate(prods):
                    if prod not in usedProds:
                        newRun = list(pRun)
                        newRun[i] = prod
                        usedProds.add(prod)
                        tmp.append(sorted(newRun))
            run = tmp         
        run.pop()
        return run


""""
okay.. still not able to deal with duplicates..

think again
maybe no need to be that baffled
the choice is at i
- I combine with last (*)
- I append to it

[2,2,3]
init: []
    at 1st 2, I cannot combine, only append [2]
    at 2nd 2, 
        I combine [4] 
            at 3, 
                I combine [12] -- now this is equal to n, skip it
                I append [4,3]
        I append [2,2]
            at 3, 
                I combine [2,6]
                I append [2,2,3] 

yep.. maybe this would work 
and I can almost see a bottom up route already 
"""


class Solution:
    def getFactors(self, n: int) -> List[List[int]]:
        @cache
        def getPrimeFactors(num):
            if num == 1 or sympy.isprime(num):
                return [num]

            res = []
            i = 2
            for i in range(2, int(math.sqrt(num))+1):
                if num % i == 0:
                    res.extend(getPrimeFactors(i))
                    res.extend(getPrimeFactors(num//i))
                    break
            return res

        primeFactors = getPrimeFactors(n)
        if primeFactors[-1] == n:
            primeFactors.pop()

        if not primeFactors:
            return None
        
        res = set()
        def f(idx, run):
            if idx>=len(primeFactors):
               res.add(tuple(sorted(run))) 
               return 

            # append 
            f(idx+1, run+[primeFactors[idx]])
            # combine 
            run.sort()
            for i in range(len(run)):
                if i>0 and run[i]==run[i-1]:
                    continue
                if run[i]*primeFactors[idx]!=n:
                    run[i] *= primeFactors[idx]
                    f(idx+1, sorted(run))
                    run[i] //= primeFactors[idx]
        
        f(0,[])
        return [list(t) for t in res]


"""

16 / 68 test cases passed. and TLE... at 8192

wow!
try to avoid duplicate
                if i>0 and run[i]==run[i-1]:
                    continue

59 / 68 test cases passed.

and TLE at 32768
okay.. so these 2 power...

ahhhhh ughhhhhh uaghauhghhh

this is a simple backtracking problem 
I wasted my life again

"""


class Solution:
    def getFactors(self, n: int) -> List[List[int]]:
        res = []
        def f(run, remain, start):
            if remain <= 1:
                if len(run) > 1:
                    res.append(list(run))
                return 
            
            for i in range(start, remain+1):
                if remain % i == 0:
                    run.append(i)
                    f(run, remain//i, i)
                    run.pop()
        f([],n,2)
        return res

"""
this is probably another blind spot for me
but it is very delicate here

e.g. 6->2,3
2,3 can be get pretty easily 
then at top level, 3 is factor of 6, when it don't get 3,2

because the start is at least i. when i is 3, the start cannot go back to 2.. 
so at top level, 3... it will end [3] and not full..

I don't know what this is.. but very werid

but 47 / 68 test cases passed and TLE at 9730007
hahahahaha....

not even better than mine..

okay.. this one is big god
"""


class Solution:
    def getFactors(self, n):
        def factor(n, i, combi, combis):
            while i * i <= n:
                if n % i == 0:
                    combis += combi + [i, n/i],
                    factor(n/i, i, combi+[i], combis)
                i += 1
            return combis
        return factor(n, 2, [], [])

"""
Runtime: 121 ms, faster than 58.56% of Python3 online submissions for Factor Combinations.
Memory Usage: 14.5 MB, less than 99.53% of Python3 online submissions for Factor Combinations.
"""


if __name__ == '__main__':
    s = Solution()
    print(s.getFactors(100))
    print(s.getFactors(12))
    print(s.getFactors(27))
    print(s.getFactors(16))
    print(s.getFactors(100))
    print(s.getFactors(90))
    print(s.getFactors(37))
