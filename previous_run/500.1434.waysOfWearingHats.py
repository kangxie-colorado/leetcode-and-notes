"""
https://leetcode.com/problems/number-of-ways-to-wear-different-hats-to-each-other/?envType=study-plan&id=dynamic-programming-iii

at least dfs is kind of clear to see?
or perhaps bitmap to store 40 hats status

then we can use cache.. 
try both



"""


from functools import cache
from typing import List


class Solution:
    def numberWays(self, hats: List[List[int]]) -> int:
        mod = 10**9+7

        def f(idx,chosen):
            if idx == len(hats):
                return 1
            
            res = 0
            for hat in hats[idx]:
                if hat not in chosen:
                    res += f(idx+1, chosen.union({hat}))%mod
            
            return res%mod
        
        return f(0,set())

"""
45 / 65 test cases passed.
and TLE... 
"""


class Solution:
    def numberWays(self, hats: List[List[int]]) -> int:
        mod = 10**9+7

        @cache
        def f(idx, chosen):
            if idx == len(hats):
                return 1

            res = 0
            for hat in hats[idx]:
                if 1<<(hat-1) & chosen == 0:
                    res += f(idx+1, chosen | (1<<(hat-1))) % mod

            return res % mod

        return f(0, 0)


class Solution:
    def numberWays(self, hats: List[List[int]]) -> int:
        hats.sort(key=lambda x:len(x))

        mod = 10**9+7

        @cache
        def f(idx, lower20, top20):
            if idx == len(hats):
                return 1

            res = 0
            for hat in hats[idx]:
                if hat < 20 :
                    if 1 << (hat-1) & lower20 == 0:
                        res += f(idx+1, lower20 | (1 << (hat-1)), top20) % mod
                else:
                    if 1 << (hat-20) & top20 == 0:
                        res += f(idx+1, lower20, top20 | (1 << (hat-20))) % mod

            return res % mod

        return f(0, 0,0)

""""
ugh.. smart ass
I try to do the bitmask on hats, which are 40.. so space is too huge
if I turn this around.. and because 1 <= n <= 10, the bitmask size becomes 10 (from 40)

it will be much more manageable !!
"""



class Solution:
    def numberWays(self, hats: List[List[int]]) -> int:
        mod = 10**9+7
        hatsPerPerson = [[] for _ in range(41)]
        for p,H in enumerate(hats):
            for h in H:
                hatsPerPerson[h].append(p)
        
        @cache
        def f(idx, peopleMask):
            if peopleMask+1 == 1<<len(hats):
                return 1
            if idx == 41:
                return 0
            if not hatsPerPerson[idx]:
                return f(idx+1, peopleMask)

            res = 0
            for p in hatsPerPerson[idx]:
                # you can give to this person or not
                # only if this person has not hat.. if he does, there is no choice for him
                if 1 << p & peopleMask == 0:
                    res += f(idx+1, peopleMask)
                    res += f(idx+1, peopleMask | 1 << p)

            # print(idx,bin(peopleMask)[2:],res)
            return res % mod

        return f(1,0)


class Solution:
    def numberWays(self, hats: List[List[int]]) -> int:
        mod = 10**9+7
        hatsPerPerson = [[] for _ in range(41)]
        for p, H in enumerate(hats):
            for h in H:
                hatsPerPerson[h].append(p)

        @cache
        def f(idx, peopleMask):
            if peopleMask+1 == 1 << len(hats):
                return 1
            if idx == 41:
                return 0

            res = 0
            for p in hatsPerPerson[idx]:
                # you can give to this person or not
                # only if this person has not hat.. if he does, there is no choice for him
                if 1 << p & peopleMask == 0:
                    res += f(idx+1, peopleMask | 1 << p)

            res += f(idx+1, peopleMask)
            return res % mod

        return f(1, 0)

"""
huh.,. this one passed
Runtime: 392 ms, faster than 66.99% of Python3 online submissions for Number of Ways to Wear Different Hats to Each Other.
Memory Usage: 41.6 MB, less than 44.66% of Python3 online submissions for Number of Ways to Wear Different Hats to Each Other.

but the above one cannot.. 
but they are the same?

ah.. okaokay..

            res = 0
            for p in hatsPerPerson[idx]:
                # you can give to this person or not
                # only if this person has not hat.. if he does, there is no choice for him
                if 1 << p & peopleMask == 0:
                    res += f(idx+1, peopleMask)
                    res += f(idx+1, peopleMask | 1 << p)


what I did was
    for each person, I add a f(idx+1, peopleMask)
    for person1 you don't give to him.. let the rest decide..
    for person2 you don't give to him.. let the rest decide..
    for person3 you don't give to him.. let the rest decide..

    so the problem is... that is some duplicates
    you either give to someone.. or no one
    you cannot 
        give to p1, not give to p1
        give to p2, not give to p2..

        cause "give to p1" will overlap with "not give to p2"
        holy ...
"""

if __name__ == '__main__':
    s = Solution()
    print(s.numberWays(hats = [[3,4],[4,5],[5]]))
    print(s.numberWays(hats=[[3, 5, 1], [3, 5]]))
    print(s.numberWays(hats = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]))
    print(s.numberWays(hats =[[1,2,3,4,5,7,9,11,12,13,17,18,19,20,21,22,23,24,25],[1,2,3,4,5,6,7,8,9,12,13,14,15,16,18,20,21,22,24,25],[2,3,7,12,13,15,19,22,23,24],[6,9,11,12,14,15,16,17,20,22,24,25],[10],[19,21,24],[1,3,5,6,8,10,11,13,14,15,16,17,18,20,22,24,25],[3,7,9]]))