"""
https://leetcode.com/problems/maximum-value-at-a-given-index-in-a-bounded-array/

low acceptance ratio
so twisty!!!!

so I can n<=maxSum
that means if n==maxSum, the max val is 1

also when a val>1 meets the condition, any smaller val would meets right
so if maxmize the val at index, can I make the array to look like (greedy)

... k-2,k-1,k,k-1,k-2...
any element is max(k-?, 1)

I then think to simplify the calculation of sum.. but do I?
ah yes, you do... 1 <= n <= maxSum <= 10^9 this is too big

I did some whiteboard calculation 
looks like the sum is related to the length of left/right, not about the index
so it can be simplified to a function as below 
f(k,l) - the min sum, start as k-1 (k is not counted in this interval)
    - if l>=k-1, the k-1,k-2... seq will fall to 1 at some time
        k*k-k(k-1)/2+(l-k+1)
        correction: there is an error should be 
        k*(k-1)-k(k-1)/2+(l-k+1) = k(k-1) + (l-k+1) 
    - if l<k-1, the k-1,k-2... seq will continue down to k-l
        k*l - l(l+1)/2
leftSum + k + rightSum will be the total sum... 

so lets give a try

"""


class Solution:
    def maxValue(self, n: int, index: int, maxSum: int) -> int:
        def minSum(k,l):
            if l>=k-1:
                return k*(k-1)//2 + l-k+1
            else:
                return k*l - l*(l+1)//2

        def ok(k):
            leftLen = index
            rightLen = n-index-1

            return minSum(k, leftLen) + k + minSum(k, rightLen) <= maxSum


        l,r = 1,maxSum

        while l<r:
            m = r-(r-l)//2
            if ok(m):
                l=m
            else:
                r=m-1
        return l

"""
Runtime: 38 ms, faster than 89.54% of Python3 online submissions for Maximum Value at a Given Index in a Bounded Array.
Memory Usage: 13.8 MB, less than 83.26% of Python3 online submissions for Maximum Value at a Given Index in a Bounded Array.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.maxValue(n=4, index=2,  maxSum=6))
