"""
feels like a two pointer -- nah, not really pointer

feels like a reverse looking
1 2 3 5
      j: 
1 2 3 7
  if A[j] <= A[j-1] and A[j] <= B[j-1], then no way to swap to make it happen
     B[j] <= B[j-1] and B[j] M= A[j-1], no way either
  otherwise, 
      if A[j] > A[j-1] or B[j] > B[j-1], no need
  otherwise,
      swap the breaking side

  now I don't think you need to start from the end
  start from the beginning the same



"""
from functools import cache
from typing import List


# class Solution:
#     def minSwap(self, nums1: List[int], nums2: List[int]) -> int:
        
#         for i, (num1, num2) in enumerate(zip(nums1, nums2)):
#             if i == len(nums1) - 1:
#                 return res
#             nextNum1, nextNum2 = nums1[i+1], nums2[i+1]
#             if num1 < nextNum1 and num2 < nextNum2:
#                 continue
            
#             if num1 >= nextNum1 and num1 >= nextNum2 and num2 >= nextNum1 and num2 >= nextNum2:
#                 return False
            
#             res += 1
#             ...

""""
ugh.. what am I doing?
the problem states it is possible to make the swap happen
asking the minimal moves.. 

what am I doing????
"""

class Solution:
    def minSwap(self, nums1: List[int], nums2: List[int]) -> int:
        
        @cache
        def f(idx,needSwap, swapLast):
            if idx >= len(nums1)-1:
                return needSwap
            
            if swapLast:
                nums1[idx-1],nums2[idx-1] = nums2[idx-1],nums1[idx-1]

            swaps = 0
            if needSwap:
                nums1[idx],nums2[idx] = nums2[idx],nums1[idx]
                swaps = 1

            if nums1[idx] < nums1[idx+1] and nums2[idx] < nums2[idx+1]:
                return f(idx+1, False, False) + swaps
            
            canSwap = nums1[idx] > nums2[idx-1] and nums2[idx] > nums1[idx-1]
            if canSwap:
                return min(1 + f(idx+1, False, True), f(idx+1, True, False)) + swaps
            
            return f(idx+1, True, False) + swaps
        
        if nums1[0] < nums1[1] and nums2[0] < nums2[1]:
            return f(1,False)
        
        return min(1+f(1,False), f(1,True))



class Solution:
    def minSwap(self, nums1: List[int], nums2: List[int]) -> int:
        
        @cache
        def f(idx,needSwap, swapLast):
            if idx == len(nums1)-1:
                return needSwap
            
            num1, num2 = nums1[idx], nums2[idx]
            last1, last2 = nums1[idx-1], nums2[idx-1]
            next1, next2 = nums1[idx+1], nums2[idx+1]

            
            if needSwap:
                num1,num2 = num2, num1
                
            if swapLast:
                last1,last2 = last2, last1

            resNoSwapThis = float('inf')
            if num1 < next1 and num2 < next2:
                resNoSwapThis = f(idx+1, False, needSwap) + needSwap
            
            resSwapNext = f(idx+1, True, needSwap) + needSwap

            canSwap = num1 > last2 and num2 > last1
            if canSwap:
                resSwapThis =  f(idx+1, False, not needSwap) # swap this
                if not needSwap:
                    resSwapThis += 1 # if this is not swapped, need to count 1; otherwise, swap twice means no swap is neede

                return min(resSwapThis, resSwapNext, resNoSwapThis)
            
            return min(resSwapNext, resNoSwapThis)
        
        res1=res2=res3=float('inf')
        if nums1[0] < nums1[1] and nums2[0] < nums2[1]:
            res1 = f(1,False, False)
        
        return min(res1, 1+f(1,False, True), f(1,True, False))

"""
this version passed 102
102 / 117 test cases passed.


class Solution:
    def minSwap(self, nums1: List[int], nums2: List[int]) -> int:
        
        @cache
        def f(idx,needSwap, swapLast):
            if idx >= len(nums1)-1:
                return needSwap
            
            num1, num2 = nums1[idx], nums2[idx]
            last1, last2 = nums1[idx-1], nums2[idx-1]
            next1, next2 = nums1[idx+1], nums2[idx+1]

            swaps = 0
            if needSwap:
                num1,num2 = num2, num1
                swaps = 1
            if swapLast:
                last1,last2 = last2, last1

            if num1 < next1 and num2 < next2:
                return f(idx+1, False, needSwap) + swaps
            
            canSwap = num1 > last2 and num2 > last1
            if canSwap:
                return min(1 + f(idx+1, False, not needSwap), f(idx+1, True, needSwap)) + swaps
            
            return f(idx+1, True, needSwap) + swaps
        
        if nums1[0] < nums1[1] and nums2[0] < nums2[1]:
            return f(1,False, False)
        
        return min(1+f(1,False, True), f(1,True, False))

"""

class Solution:
    def minSwap(self, nums1: List[int], nums2: List[int]) -> int:
        
        @cache
        def f(idx,needSwap, swapLast):
            if idx >= len(nums1)-1:
                return needSwap
            
            num1, num2 = nums1[idx], nums2[idx]
            last1, last2 = nums1[idx-1], nums2[idx-1]
            next1, next2 = nums1[idx+1], nums2[idx+1]

            swaps = 0
            if needSwap:
                num1,num2 = num2, num1
                swaps = 1
            if swapLast:
                last1,last2 = last2, last1

            if num1 < next1 and num2 < next2:
                return min(f(idx+1, True, needSwap), f(idx+1, False, needSwap)) + swaps
            
            canSwap = num1 > last2 and num2 > last1
            if canSwap:
                return min(1 + f(idx+1, False, not needSwap), f(idx+1, True, needSwap)) + swaps
            
            return f(idx+1, True, needSwap) + swaps
        
        if nums1[0] < nums1[1] and nums2[0] < nums2[1]:
            return f(1,False, False)
        
        return min(1+f(1,False, True), f(1,True, False))


""""
okay.. DP

dp[i][0]: no swap at i, and min-moves to keep A[:i+1] and B[:i+1] strictly sorted
dp[i][j]: do swap at i, and min-moves to keep A[:i+1] and B[:i+1] strictly sorted

dp[i] <= dp[i-1]: dp[i] only depends on dp[i-1]

and dp[i][0] can be updated
(no change this round)

A[i] > A[i-1] and B[i] > B[j-1]
  dp[i][0] = min(dp[i][0], dp[i-1][0]) # i-1 round, no swap either

A[i] > B[i-1] and B[i] > A[j-1]
  dp[i][0] = min(dp[i][0], dp[i-1][1]) # i-1 round, swapped

# this round can change - dp[i][1]

B[i] > A[i-1] and A[i] > B[j-1]
  # last round no change
  dp[i][1] = min(dp[i][0], 1+dp[i-1][0])

B[i] > B[i-1] and A[i] > A[j-1]
  # last round also swapped
  dp[i][1] = min(dp[i][0], 1+dp[i-1][1])
  

I have walked into wrong direction so it is not so straight to understand
I have figured out, only this two positions would matter
A:  l1 n1
B:  l2 n2

the ONLY eligible combinations are 
l1<n1 and l2<n2 (no change last round, not change this round)
A:  l1 n1
B:  l2 n2

l1<n2 and l2<n1 (no change last round, change this round)
A:  l1 n2
B:  l2 n1

l2<n1 and l1<n2 (change last round, no change this round)
A:  l2 n1
B:  l1 n2

l2<n2 and l1<n1 (change last round, change this round)
  this seems confusing but the sequence is like
A: l2 n2
B: l1 n2


"""


class Solution:
    def minSwap(self, A: List[int], B: List[int]) -> int:
        # dp[0][i]: no swap
        # dp[1][i]: swap
        dp = [[float('inf')]*len(A) for _ in range(2)]
      
        dp[0][0] = 0
        dp[1][0] = 1

        for i in range(1,len(A)):
            # no-swap this round
            if A[i] > A[i-1] and B[i] > B[i-1]:
                # can come from no-swap last round
                dp[0][i] = min(dp[0][i], dp[0][i-1])
            
            if A[i] > B[i-1] and B[i] > A[i-1]:
                # can come from swap last round
                dp[0][i] = min(dp[0][i], dp[1][i-1])
            
            # swap this round
            if B[i] > A[i-1] and A[i] > B[i-1]:
                # can come from no-swap last round
                dp[1][i] = min(dp[1][i], 1+dp[0][i-1])
            
            if B[i] > B[i-1] and A[i] > A[i-1]:
                # can come from swap last round
                dp[1][i] = min(dp[1][i], 1+dp[1][i-1])
        return min(dp[0][-1], dp[1][-1])

class Solution:
    def minSwap(self, A: List[int], B: List[int]) -> int:
        
        def f(i):
            if i==0:
                return 0,1
            
            noSwap = swap = float('inf')
            noSwap_prev, swap_prev = f(i-1)
            if A[i] > A[i-1] and B[i] > B[i-1]:
                noSwap = min(noSwap, noSwap_prev)
                        
            if A[i] > B[i-1] and B[i] > A[i-1]:
                # can come from swap last round
                noSwap = min(noSwap, swap_prev)
            
            # swap this round
            if B[i] > A[i-1] and A[i] > B[i-1]:
                # can come from no-swap last round
                swap = min(swap, 1+noSwap_prev)
            
            if B[i] > B[i-1] and A[i] > A[i-1]:
                # can come from swap last round
                swap = min(swap, 1+swap_prev)
            return noSwap,swap
      
        noswap,swap = f(len(A)-1)
        return min(noswap,swap)

if __name__ == '__main__':
        s = Solution()
        # print(s.minSwap(nums1 = [1,3,5,4], nums2 = [1,2,3,7]))
        print(s.minSwap(A = [3,3,8,9,10], B = [1,7,4,6,8]))
          
        
        