"""
https://leetcode.com/problems/sell-diminishing-valued-colored-balls/?envType=study-plan&id=binary-search-ii

not very easy I did it after looking at the hints
just record my thoughts (copy from submissions)
"""

# naive heap TLE quickly


import bisect
import heapq
from typing import List


class Solution:
    def maxProfit(self, inventory: List[int], orders: int) -> int:
        # feeling like a heap problem?

        h = []
        for ball in inventory:
            heapq.heappush(h, -ball)

        res = 0
        while orders:
            ball = heapq.heappop(h)
            res -= ball
            ball += 1
            heapq.heappush(h, ball)
            orders -= 1
        return res

# then thought
class Solution:
    def maxProfit(self, inventory: List[int], orders: int) -> int:
        # feeling like a heap problem?
        
        h = []
        for ball in inventory:
            heapq.heappush(h, -ball)
        
        res = 0
        while orders:
            ball = heapq.heappop(h)
            res -= ball
            ball += 1
            heapq.heappush(h, ball)
            orders-=1
        return res


# then I thought went as below
        # using heap it times out easily
        # thinking again
        # after sort
        # [n1,n2,n3]
        # first notice I can take n3-n2 without consequence
        # the beginning value is n3, the end values is n2 (n2+..+n3)

        # then it becomes [n1,n2,n2]
        # then I can take n2-n1 (*2) without consequnce
        # the beginning value is n2, the end values is n1 (n1+..+n2) * 2
        # so on and so forth?

        # then when every becomes [n1,n1,n1]
        # I can take one from every one.. if the order remain allows
        # otherwise.. I need to stop somewhere

        # I wouldn't be able to code this idea up now...
        # just submit and hopefully it remembers


# I touched one correct aspects by above
# and then
        # following the hints
        # 1,2,2,4,5,5,5,6,7
        # if k=3, order=14
        # bisect_left(a,3) -> 3
        # then every number [3:] first becomes 3
        # prefix sum: [0,1,3,5,9,14,19,24,30,37]
        # [3:] has 6 element
        # each element contribute something related to its val: v
        # v>3: v,v-1,4 (to k+1)
        # totalSum of [v->1] is v(v+1)//2
        # k -> 1.. k(k+1)//2, if k==3, the this is 3
        # so total sell values for
        # 4: 4*5//2=10 - 3*4//2=6 = 4
        # 4: 15-6=9 (5+4)
        # 7: 7*8//2=28 - 6 = 22 (7+6+5+4)
        # okay.. this part checks out
        # the total will be

        # total=0; for v in A[idx:]
        #   total += v*(v+1)//2 - k(k+1)//2
        # but how many balls are sold here
        # it is prefixSum - no*k = 37-5 - 6*3 = 14
        # from [3:], 1,2,2,4,5 => 14 yep

        # so the sold balls are rangeSum - k*value + ?
        # the total value you sell is
        # total=0; for v in A[idx:]
        #   total += v*(v+1)//2 - k(k+1)//2

        # the hints are bout searching k
        # so if at given k, the order can be reached
        # then for a smaller k, the order can be easily satisfied..
        # when the k is 7, you can only sell 1 ball
        # when the k is 1, can sell many balls...
        # and apparently, when k is bigger, with k being the smallest sell price..
        # and order number needs to be met.. so we also want the biggest k

        # biggest k to meet the order number
        # do a wrong answer to keep my notes

# getting closer

class Solution:
    def maxProfit(self, A: List[int], orders: int) -> int:
        n = len(A)
        mod = 10**9 + 7
        A.sort()

        # so the sold balls are rangeSum - k*value + ?
        # the total value you sell is
        # total=0; for v in A[idx:]
        #   total += v*(v+1)//2 - k(k+1)//2
        # biggest k to meet the order number

        # continue to explore
        # 1,2,2,4,5,5,5,6,7
        # idx = bisect_left(a, k), left or right?
        # if the k=2, bisect_left will land on idx-1
        # but the 2s are waste
        # so maybe it should be bisect_right... yes.. bisect_right feels better
        # rangeSum is the summ[-1] - summ[idx]

        # idx = 3, the first >=k is idx 3
        # then the minus part in the rangeSum is idx-3 (in summ)
        # and the v is also starting from 3
        # worthy some try now

        summ = [0]*(n+1)
        for i in range(1, n+1):
            summ[i] = summ[i-1] + A[i-1]

        def canSellEnough(k):
            idx = bisect.bisect_left(A, k)
            sellAboveK = summ[-1] - summ[idx] - (n-idx)*k
            # print(idx, sellAboveK, k, l,r)

            # idx to the right are >k... (because bisect_right)
            # therefore they >A[idx-1], which at most can be k
            # so they can sell one more.. and not violate the rules
            # the total sell-able balls with lowest value being k  is
            # sellAboveK + (n-idx)

            # return
            # total possible sell >= needed
            # the idx to start and extra number of k values taken
            # print(sellAboveK + (n-idx) >= orders, idx, orders-sellAboveK)
            return sellAboveK + (n-idx) >= orders, idx, orders-sellAboveK

        # l,r represnt the possible k values
        # it can be 0.. sell everything
        # at most it can be max(A)... sell only the biggest
        l, r = 0, A[-1]
        while l < r:

            m = r-(r-l)//2

            ok, idx, extraC = canSellEnough(m)
            if ok:
                l = m
                # a big trap awaits: the extra is only valid when ok is true
                # or alternatively, we should call the canSellEnough(l) after binary search
                # like that sumUnderK()
                extra = extraC
            else:
                r = m-1

        # with l-the k value and idx, calculate the total order
        # total=0; for v in A[idx:]
        #   total += v*(v+1)//2 - k(k+1)//2
        # print(idx,l,extra)
        total = 0
        for v in A[idx:]:
            total += v*(v+1)//2 - l*(l+1) // 2
        total += extra*l
        return total % mod

# I still struggle with bisect_right vs bisect_left
# and the ok.idx.extraC got overriden by last invalid run.. 
# that is tricky 
# some good idiom is really important..
# remember in binary search, the finished blow might go two two branches.. so don't rely on it for some final state

# and final version


class Solution:
    def maxProfit(self, A: List[int], orders: int) -> int:
        n = len(A)
        mod = 10**9 + 7
        A.sort()

        # so the sold balls are rangeSum - (n-idx)*k + ?
        # the total value you sell is
        # total=0; for v in A[idx:]
        #   total += v*(v+1)//2 - k(k+1)//2
        # also plus some extra sold k-valued balls 
        #   total += extra * k
        #   extra = order - rangeSum - k*value
        # biggest k to meet the order number

        # continue to explore
        # 1,2,2,4,5,5,5,6,7
        # idx = bisect_left(a, k), left or right?
        # after reasoning and trapping... it should be bisect_left

        summ = [0]*(n+1)
        for i in range(1, n+1):
            summ[i] = summ[i-1] + A[i-1]

        def canSellEnough(k):
            idx = bisect.bisect_left(A, k)
            sellAboveK = summ[-1] - summ[idx] - (n-idx)*k
            # print(idx, sellAboveK, k, l,r)
            # the equal == k values will not make impact to sellAboveK
            # but they contribtue to extra part
            # return following
            #   total possible sell >= needed
            #   the idx to start
            # print(sellAboveK + (n-idx) >= orders, idx, orders-sellAboveK)
            return sellAboveK + (n-idx) >= orders, idx

        # l,r represnt the possible k values
        # it can be 0.. sell everything
        # at most it can be max(A)... sell only the biggest
        l, r = 0, A[-1]
        while l < r:

            m = r-(r-l)//2
            if canSellEnough(m)[0]:
                l = m
                # a big trap awaits: the extra is only valid when ok is true
                # or alternatively, we should call the canSellEnough(l) after binary search
                # like that sumUnderK()
                # so I moved to the end to re-compute
            else:
                r = m-1

        # with l-the k value and idx, calculate the total order
        # total=0; for v in A[idx:]
        #   total += v*(v+1)//2 - k(k+1)//2
        # print(idx,l,extra)
        total = 0
        idx = canSellEnough(l)[1]
        for v in A[idx:]:
            total += v*(v+1)//2 - l*(l+1) // 2

        sellAboveK = summ[-1] - summ[idx] - (n-idx)*l
        total += (orders-sellAboveK)*l
        return total % mod
