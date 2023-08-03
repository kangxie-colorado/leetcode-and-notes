"""
https://leetcode.com/problems/non-negative-integers-without-consecutive-ones/?envType=study-plan&id=dynamic-programming-iii

had no idea but see the similar question to be house robber
then... 
hmm.. yeah.. it is just to avoid robbing two adjacent houses.. (setting 1 to two bits)

might just turn it into a str to work with
"""


from functools import cache



class Solution:
    def findIntegers(self, n: int) -> int:
        n = bin(n)[2:]

        @cache
        def f(idx, run):
            # print(idx,run)
            if run > n:
                return 0
            if idx == -1:
                return 1

            # not setting to 1
            res = f(idx-1, run)
            if idx+1 == len(n) or run[idx+1] == '0':
                res += f(idx-1, run[:idx]+'1'+run[idx+1:])

            # print(res)
            return res
        return f(len(n)-1, '0'*len(n))

"""
right.. but cannot pass really even with cache

1: 2
2: 3
3: 3
4: 4
5: 5
6: 5
7: 5
8: 6
9: 7
"""


class Solution:
    def findIntegers(self, n: int) -> int:
        nStr = bin(n)[2:]

        @cache
        def f(idx, run):
            # print(idx,run)
            if run > n:
                return 0
            if idx == -1:
                return 1

            # not setting to 1
            res = f(idx-1, run)
            if idx+1 == len(nStr) or (1 << len(nStr)-idx-2) & run == 0:
                res += f(idx-1, (1 << len(nStr)-idx-1) |run)

            # print(res)
            return res
        return f(len(nStr)-1, 0)

"""
okay stuck
checked the solution tab.. and it is brilliant

f(n) = f(n-1) w/ 1
    +  f(n-2) 2/ 01

then I was wondering how to bitmask '01' << x?
turns out I can just jump the index...
"""


class Solution:
    def findIntegers(self, n: int) -> int:
        nStr = bin(n)[2:]

        @cache
        def f(idx, run):
            # print(idx,run)
            if run > n:
                return 0
            if idx < 0:
                return 1

            # not setting to 1 or setting to 1 then jump 2 
            res = f(idx-1, run) + f(idx-2, (1 << len(nStr)-idx-1) | run)

            # print(res)
            return res
        return f(len(nStr)-1, 0)

"""
do I need run parameter?
I need run to keep the invliad number out
"""


class Solution:
    def findIntegers(self, n: int) -> int:

        def f(num):
            if num>n:
                return 0
            if num&1:
                return 1+f(num<<1)        
            else:
                return 1+f(num<<1)+f(num<<1|1)

        return f(1)+1

"""
okay.. here comes the genius
class Solution:
    def findIntegers(self, num):
        x, y = 1, 2
        res = 0
        num += 1
        while num:
            if num & 1 and num & 2:
                res = 0
            res += x * (num & 1)
            num >>= 1
            x, y = y, x + y
        return res

Runtime: 37 ms, faster than 62.07% of Python3 online submissions for Non-negative Integers without Consecutive Ones.
Memory Usage: 13.8 MB, less than 71.72% of Python3 online submissions for Non-negative Integers without Consecutive Ones.

from whom you ask? Lee

would be interesting to read up some discussions
I apparently have not a lot idea..
"""

if __name__ == '__main__':
    s = Solution()
    print(s.findIntegers(1000000000))
    print(s.findIntegers(5))
    print(s.findIntegers(1))
    print(s.findIntegers(2))
    print(s.findIntegers(6))
