"""
https://leetcode.com/problems/minimum-absolute-sum-difference/

the dark side of binary search 
so by the thoughts train.. I should search for the target sum which is between 0 and sum(A)+sum(B) (don't really matter too much, as long as it is big enough)

what is the monotonicity???
hmm...

let me think brute force first?
replace at most one.... no-replace and one-replace
for any element, I can use it to replace other n-1 element 
it will (n-1)^n.. not possible to solve it this way

let me see
the original diff is 

sum([a,b for a,b in zip(A,B)])

I will change A[i] to A[j]..
so what changed in the sum

abs(B[j] - A[j]) => abs(B[j]-A[i]) = abs(B[j]-A[j] + (A[j]-A[i])) =  abs(B[j]-A[j] + delta_j_i)
also this eqaul to ?
    if B[j]>=A[j]:
        abs(B[j]-A[j]) + abs(delta_j_i)
    else:
        abs(B[j]-A[j]) -  abs(delta_j_i)
okay.. this cannot go anywhere.. just focus on the whole

for other k, k!=j, the diff does't change
so the search is to search a i,j to have abs(B[j]-A[j] + delta_j_i) to the minimun 

B[j]-A[i]  can be calculated easily 
then it is to find i,j pair in A to make this abs minimum 

A = [1,7,5], B = [2,3,5]
B-A = [1,-4,0]

then I binary search the delta????
fix j? search i?

j=0.. i=? 
    i=0 no change
    i=1 1-7 = -6, 1+(-6) = 5.. getting bigger
j=1...

j=2...

n**2?!?

if I sort B-A by abs() and reverse

[-4,1,0]
I want to minimize the biggest one.. 
---

maybe no need to calculate the B-A
A = [1,7,5], B = [2,3,5]
still fix j, search i

if j points to 3, then in A, j points to 7, 
so basically I want to search in A - 3... [-2,4,2].. search the smallest abs()

maybe not binary search but at least something better than n**2
let me code first 


"""


import bisect
from typing import List


class Solution:
    def minAbsoluteSumDiff(self, A: List[int], B: List[int]) -> int:
        n = len(A)
        origDiff = sum([abs(a-b) for a,b in zip(A,B)])

        # fix j, search i
        for b in B:
            # search in A - [b]*n for the abs() min
            # but this is O(n) or if you search O(nlogn) 
            # and the outer loop is O(n) so O(n**2) or O(n**2 * logn)
            # okay.. looks like I need to sort A first

            ...


"""
so combine A and B, sort AB.. 
then fix j to search i.. now we can do binary search
"""
class Solution:
    def minAbsoluteSumDiff(self, A: List[int], B: List[int]) -> int:
        mod = 10**9 + 7
        n = len(A)
        origDiffSum = sum([abs(a-b) for a, b in zip(A, B)])
        AB = sorted([(a, b) for a, b in zip(A, B)])
        res = float('inf')

        # fix j, search i
        for a, b in AB:
            # search b in AB.. so it is actually search in A (but I need to carry the mapping relationship)
            idx = bisect.bisect_left(AB, (b, 0))  # search (b,0) so no conflict
            # look left, look right
            leftVal = AB[idx-1][0] if idx > 0 else float('inf')
            rightVal = AB[idx][0] if idx < n else float('inf')

            # i will be leftVal or rightVal
            origDiff = abs(b-a)
            newDiff = min(abs(b-leftVal), abs(b-rightVal))
            res = min(res, origDiffSum - origDiff + newDiff)

        return res % mod

"""
Runtime: 1305 ms, faster than 71.02% of Python3 online submissions for Minimum Absolute Sum Difference.
Memory Usage: 34.6 MB, less than 11.36% of Python3 online submissions for Minimum Absolute Sum Difference.
"""

if __name__ == '__main__':
    print(Solution().minAbsoluteSumDiff(A=[1, 7, 5], B=[2, 3, 5]))
    print(Solution().minAbsoluteSumDiff(
        A=[2, 4, 6, 8, 10], B=[2, 4, 6, 8, 10]))
    print(Solution().minAbsoluteSumDiff(
        A=[1, 10, 4, 4, 2, 7], B=[9, 3, 5, 1, 7, 4]))
