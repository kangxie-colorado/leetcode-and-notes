"""
https://leetcode.com/problems/minimum-cost-to-hire-k-workers/

okay.. I don't know how to do this
this came up in a mock assessment interview

I failed it.. but decided to learn it back

"""


# the brute force...
# okay.. I know its TLE... but it lays the foundation for thinking about this problem
# using every worker as captain to calculate the unit cost (wage/quality)
# then going thru the list see each/every one cost
# if the price end up smaller than min-wage.. no-can-do
# if after all going thru.. there are at least k workers that can be met with their requirements
# it will be a candidate and take the first K worker and sum their pay up...
# yeah.. the thinking is natural but I failed to grasp this at all

from collections import defaultdict
import heapq
from typing import List


class Solution(object):
    def mincostToHireWorkers(self, quality, wage, K):
        from fractions import Fraction
        ans = float('inf')

        N = len(quality)
        for captain in range(N):
            # Must pay at least wage[captain] / quality[captain] per qual
            factor = Fraction(wage[captain], quality[captain])
            prices = []
            for worker in range(N):
                price = factor * quality[worker]
                if price < wage[worker]:
                    continue
                prices.append(price)

            if len(prices) < K:
                continue
            prices.sort()
            ans = min(ans, sum(prices[:K]))

        return float(ans)


"""
reading the offical solution.. like a shit
then Lee's

"1. Every worker in the paid group should be paid in the ratio of their quality compared to other workers in the paid group."
So for any two workers in the paid group,
we have wage[i] : wage[j] = quality[i] : quality[j]
So we have wage[i] : quality[i] = wage[j] : quality[j]
We pay wage to every worker in the group with the same ratio compared to his own quality.

holy..grail.. this transtiion immediately clears the cloud that the ratio must be consistent across the board

"2. Every worker in the paid group must be pa   id at least their minimum wage expectation."
For every worker, he has an expected ratio of wage compared to his quality.


So to minimize the total wage, we want a small ratio.
So we sort all workers with their expected ratio, and pick up K first worker.
Now we have a minimum possible ratio for K worker and we their total quality.

okay.. total quality*the-expected-but-valid-ratio is the cost
"""


def mincostToHireWorkers(self, quality, wage, K):
    workers = sorted([float(w) / q, q] for w, q in zip(wage, quality))
    res = float('inf')
    qsum = 0
    heap = []
    for r, q in workers:

        heapq.heappush(heap, -q)
        qsum += q
        if len(heap) > K:
            # okay don't get confused here.. because the heap store negative, so this is actually minus q
            qsum += heapq.heappop(heap)
        if len(heap) == K:
            # okay.. I see.. because workers are sorted by ratio..
            # so r[2]>r[1]
            # r[k] > r[0..k-1].. with r[k], all the workers requirement can be satisfied
            res = min(res, qsum * r)
    return res


"""
then I am thinking why cannot I use two max heap
one just like the heap in here
another just to sort out the biggest ratio

but that is basically the same as what the algorithm does
just in my own way
"""


class Solution:
    def mincostToHireWorkers(self, quality: List[int], wages: List[int], k: int) -> float:
        qualPointsHeap = []
        ratioHeap = []

        totalQualPoints = 0
        res = float('inf')
        for q, w in zip(quality, wages):
            totalQualPoints += q
            heapq.heappush(qualPointsHeap, -q)
            heapq.heappush(ratioHeap, (-w/q, -q))

            if len(qualPointsHeap) > k:
                discard = heapq.heappop(qualPointsHeap)
                totalQualPoints += discard

                if ratioHeap[0][-1] == discard:
                    heapq.heappop(ratioHeap)

            if len(qualPointsHeap) == k:
                res = min(res, -totalQualPoints*ratioHeap[0][0])
        return res


"""
WRONG---

when the work has left the heap.. the ratio is still there... 
perhaps.. I can add a set to track it
"""


class Solution:
    def mincostToHireWorkers(self, quality: List[int], wages: List[int], k: int) -> float:
        qualPointsHeap = []
        ratioHeap = []

        totalQualPoints = 0
        res = float('inf')
        discards = defaultdict(int)
        for q, w in zip(quality, wages):
            totalQualPoints += q
            heapq.heappush(qualPointsHeap, (-q, -w/q))
            heapq.heappush(ratioHeap, (-w/q, -q))

            if len(qualPointsHeap) > k:
                discard, ratio = heapq.heappop(qualPointsHeap)
                totalQualPoints += discard
                discards[(ratio, discard)] += 1

                r2, d2 = ratioHeap[0]
                if discards[(r2, d2)] > 0:
                    heapq.heappop(ratioHeap)
                    discards[(r2, d2)] -= 1

            if len(qualPointsHeap) == k:
                res = min(res, -totalQualPoints*ratioHeap[0][0])
        return res


"""
 quality = [3,1,10,10,1], wage = [4,8,2,2,7], k = 3

 okay.. just in this case, the ratio 8/1 is the biggest one
 but it will dominate.. and that is wrong

 so the candidates pool should have following qualities
 1. its ratio will be kept at min possible
 2. then we can calculate a res 
    a. then we can shuffle in, shuffle out
    b. doing this, the ratio is increasing (but the quality might decrease)
        so the new-shuffle-in could stay in the pool
    c. if the new-shuffe-in bring high quality and high ratio
        then it will immediately leave and not impact the previous min-res

so yeah.. kind of mind twist...
"""


if __name__ == "__main__":
    quality = [10, 20, 5]
    wages = [70, 50, 30]
    k = 2

    print(Solution().mincostToHireWorkers(quality, wages, k))
    print(Solution().mincostToHireWorkers([3, 1, 10, 10, 1],
                                          [4, 8, 2, 2, 7],
                                          3))
