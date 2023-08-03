"""
https://leetcode.com/problems/range-sum-of-sorted-subarray-sums/

I solved this before but don't have any idea how to solve it now..
hmm... 


one way to do it is of course calculate all the subarry sums..
which would take O(n**2)

hmm... because all the numbers are postivie 
that means there can be no equal number in the prefix sum
[1,2,3,4]

[1,3,6,10]
summ(i,j) = sum[j] - sum[i-1] # if i<0, sum[i] => 0 
summ[0,0] = sum[0]
summ[1,1] = sum[1] - sunm[0] = 2

it seems like if I padding it will be better

so 
[0,1,3,6,10]

now summ[i,j] = sum[j] - sum[i-1]
but for sum[1] means sum up to 1st element -- which 1st element is the 0-idx in original array 
sum[2] means up to 2nd element 

summ[1,2] means the sum of 1-2 elements.. that is sum[2] - sum[0]
so this is range sum.. 

fix i search j again?
hmm.... totally have no idea.. how did I solve it? did i do it myself?

okay.. I see.. 
I solved using heap, which I model this like a matrix 
also that binary search.. 

f(right) - f(left-1)
f(i) the total sum up to i-th subarry sum (this is easily undersood)

then I use binary search to find 
- given a target sum, how many sums <= this target 
- and the total sum of these sums... 

that can be achieved by a sliding window technique 
- when the windSum is greater, shrink; same time shrink the total sum to be added 
- if the windSum is smaller or equal than target, then 
    update the count, which is used to steer the binary search direction 
    update the total sum, which would be used for final calculation 

hopefully I can still write it right 
"""


from typing import List


class Solution:
    def rangeSum(self, nums: List[int], n: int, left: int, right: int) -> int:
        minNum, sumNum = min(nums), sum(nums)

        def coundAndTotal(m):

            i = j = 0
            count = windSum = total = sumOfWindEndingJ = 0

            while j < n:
                windSum += nums[j]
                sumOfWindEndingJ += nums[j] * (j-i+1)
                while i < n and windSum > m:
                    # this is the most tricky part: when i slides out
                    # e.g. 1,2,3,
                    #      i   j
                    # when i slides out, it takes out wind-[1,2,3], not 1*3
                    # the windows ending at J are [1,2,3] [2,3] [3]
                    sumOfWindEndingJ -= windSum
                    windSum -= nums[i]
                    i += 1

                # i could be j+1
                # so count could += 0.. no change
                count += j-i+1
                total += sumOfWindEndingJ
                j += 1

            return count, total

        def totalSumUpto(rank):
            if rank == 0:
                return 0

            l, r = minNum, sumNum
            while l < r:
                m = l + (r-l)//2
                count, _ = coundAndTotal(m)
                if count == rank:
                    l = m
                    break
                elif count < rank:
                    l = m+1
                else:
                    r = m
            cnt, s = coundAndTotal(l)
            # the sum can be duplicate..
            # [1, 2, 3, 3, 4, 5, 6, 7, 9, 10], 3 appears twice
            # thus when you ask for rank-3, and the coverge will end at 2nd 3
            # thus one more 3..
            # l,r represent the possible sum.. it has some relationship with ranking
            # but not one-to-one. sum-3 has two rankings...
            # because 2 3s.. so it will not converge at 2 or 4.. but the 2nd 3...
            return s - (cnt-rank)*l

        return (totalSumUpto(right) - totalSumUpto(left-1)) % (10**9+7)

"""
Runtime: 85 ms, faster than 98.77% of Python3 online submissions for Range Sum of Sorted Subarray Sums.
Memory Usage: 13.9 MB, less than 96.72% of Python3 online submissions for Range Sum of Sorted Subarray Sums.

"""

if __name__ == '__main__':
    s = Solution()
    print(s.rangeSum(nums = [1,2,3,4], n = 4, left = 1, right = 5))