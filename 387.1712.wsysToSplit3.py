"""
https://leetcode.com/problems/ways-to-split-array-into-three-subarrays/?envType=study-plan&id=binary-search-ii

interesting problem
so brute force - there are n-1 positisions to place the bar 
total possibilities: (n-2) + (n-3)... O(n**2)

now I know this could be a binary search problem
how to model that?
l,r represents the ways to split 

but give a m, how do I verify?

some observations appear now?
    I can take one num for first group
    then it becomes a sub-problem: divide the rest into 2 to meet the condition but min is the first group's sum
    f(2,0) # ways of placing 2 bars 
        A[0], f(1, A[1:], minSum) (minSum = A[0])
                f(0, A[2:], minSum=A[1]) # if A[1]>=A[0] else it has to count 
                    then if sum(A[2:])>=minSum: return 1
                back track?

but this seems like a backtrack problem..
backtrack cannot solve this big scope.. there are some shortcut.. 
if the runningSum is already >=.. the plus the rest will be also qualified but this only applies to the last group 
        
ah. I see.. the binary search might be searching the prefix sum.. the pair pattern
not search how many ways to separate the array

such a twist.. 

with that in mind.. let me re-consider 
nums:           [1,2,2,2,5,0]
prefixSums:     [1,3,5,7,12,12]

now search i(i>=i) and j(j>=2) in this group to meet that condition 
1,3,5,7,12,12
  i j
sum1 = summ[i-1]
sum2 = summ[j-1] - summ[i-1]
sum3 = summ[-1] - summ[j-1]

fix i: I fix sum1, which is summ[i-1]
    search sum2 >= sum1
        i.e. summ[j-1] - summ[i-1] >= sum[i-1]
        i.e. summ[j-1] >= summ[i-1]*2
    search sum3 >= sum2
        i.e. summ[-1] - summ[j-1] >= summ[j-1] - summ[i-1]
             2*summ[j-1] <= summ[-1] + summ[i-1]
        i.e. summ[j-1] <=  (summ[-1] + summ[i-1])/2

    i.e. fix i and search j(j-1) for 2*sum[i-1] <= sum[j-1] <= (summ[-1] + summ[i-1])/2

let me see i=1, sum[i-1]... ah.. it is annoying to -1 always
if I pad the prefixsums

[0,1,3,5,7,12,12]
and i is continue to be from the origin number
then summ[1] happens to corresponds to when i points to 2 (idx-1)

so the search is 
    fix i, search for j where 2*sum[i] <= sum[j] <= (sum + sum[i])//2
    if i is at 1, 
        sum1 = summ[1] = 1
        totalSum = 12

        search j, where summ[j] in [2, (12+2)/2=6]
        for 2. I search bisect.right and got idx-2(3) (shoule be bisect.left)
        for 7 I search bisect.left and got idx-4(7).. therefore 2 possibilies 



    move i to 2
        sum1 = summ[2] = 3

        search j, [6,(12+3)/2=7]
        idx-4 (7) vs idx-4(7).. which is zero.. 
        hmm.. the bisect_left/right use is not right... hum.. sum[j] >= 2*sum[i]
        I search 2*sum[i] which is the lower bound.. seems like to be bisect_left 
        if bisect_left(6) = 4
        bisect_right(7) = 5
        then this is 1
 
 a little messed up.. let me re-focus on the prefix sum array only 
 [0,1,3,5,7,12,12] ([1,2,2,2,5,0] for reference)
 i points the last element of first group
 j points to the last element of 2nd group

 summ[i] is the group ending at i
 summ[j]-summ[i] is the group ending at j
 the last group summ is natuaraly totalSum - sum[j]

the condition to meet is 
sum[i] <= sum[j] - sum[i] <= total - sum[j]

I can get sum[j] >= 2*sums[i]
and sums[j] <= (total+sum[i])/2

aha.. I see what is wrong
    search j, where summ[j] in [2, (12+2)/2=7] -- it should "[2, (12+1)/2=6]"
    fix i at 1,  I search j in [2,6]
        bisect_left(2) => 2
        bisect_right(6) => 4
        4-2 = 2

    fix i at 3, I search j in [6, 7]
        bisect_left(6) = 4
        bisect_right(7) = 5
        5-4 = 1
    
    fix i at 5,  I serach j in [10, (12+5)/2=7].. which is not possible at all 
    the latter will all be not possible 

checking another one - [1,1,1]
prefix  0,1,2,3

    i->1, search j in [2,2]
    bisect_left(2) = 1
    bisect_right(2) = 2
    2-1..

    i->2, search j in [4,(3+2)/2=2] .. not possible 

yet one more - [3,2,1]
prefix 0,3,5,6

    i->3, serach j in [6,2] not possible.. 




"""


import bisect
from typing import List


class Solution:
    def waysToSplit(self, nums: List[int]) -> int:
        mod = 10**9+7
        summ = [0] * (len(nums)+1)

        for i in range(1, len(nums)+1):
            summ[i] = summ[i-1] + nums[i-1]

        res = 0
        total = summ[-1]
        for i in range(1, len(summ)-2):
            sum1 = summ[i]

            count = bisect.bisect_right(summ, (total+sum1)//2) - \
                max(bisect.bisect_left(summ, 2*sum1), i+1)
            if count > 0:
                res += count

        return res % mod


"""
pass 
83 / 88 test cases passed.


0,3,3 let me see

0 0 3 6
when i->0.. search [0,3]
>>> a=[0,0,3,6]
>>> bisect.bisect_left(a,0)
0
>>> bisect.bisect_right(a,3)
3

hmm... indeed something wrong
edge cases

change to this 
            count = bisect.bisect_right(summ, (total+sum1)//2) - \
                max(bisect.bisect_left(summ, 2*sum1), i+1)
            if count > 0:
                res += count

but around 0.. I still have issues

[0,0,0] should be 1 I got 2
maybe I should add 0.5 somewhere

aha..

            
            count = min(bisect.bisect_right(summ, (total+sum1)//2),len(nums))- \
                max(bisect.bisect_left(summ, 2*sum1), i+1)

            the summ is len(nums)+1, but the j cannot go out of bound (actually cannot even point to last elemnet to leave at least one element )
            so max is len(nums)-2, thus in summ it should be len(nums)-1 
            but this is bisect_right.. so len(nums) should be good

so many subtlities 
Runtime: 1596 ms, faster than 77.30% of Python3 online submissions for Ways to Split Array Into Three Subarrays.
Memory Usage: 26.8 MB, less than 99.71% of Python3 online submissions for Ways to Split Array Into Three Subarrays.
"""


class Solution:
    def waysToSplit(self, nums: List[int]) -> int:
        mod = 10**9+7
        summ = [0] * (len(nums)+1)

        for i in range(1, len(nums)+1):
            summ[i] = summ[i-1] + nums[i-1]

        res = 0
        total = summ[-1]
        for i in range(1, len(summ)-2):
            sum1 = summ[i]
            if sum1*2 > (total+sum1)//2:
                break

            count = min(bisect.bisect_right(summ, (total+sum1)//2), len(nums)) - \
                max(bisect.bisect_left(summ, 2*sum1), i+1)
            if count > 0:
                res += count

        return res % mod

"""
Runtime: 1239 ms, faster than 92.24% of Python3 online submissions for Ways to Split Array Into Three Subarrays.
Memory Usage: 27.4 MB, less than 33.33% of Python3 online submissions for Ways to Split Array Into Three Subarrays.

after adding that early termination 
"""
