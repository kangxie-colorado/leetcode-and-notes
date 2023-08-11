from typing import List


class Solution:
    def checkArray(self, nums: List[int], k: int) -> bool:
        
        for i in range(len(nums)+1-k):
            c = nums[i]
            if not c: continue
            for j in range(k):
                nums[i+j] -= c
                if nums[i+j] < 0:
                    return False
                
        return all(not num for num in nums)

"""
TLE.. O(k*n)
so that idea of diff array? what is it?

like turning the idea of O(k*n) into O(n)
I may have get the idea... basically 
at idx, the diff is -nums[idx] to get to zero
at idx+k (if <len()) 
...

watch the video again
he said, for an interval to add some number as a whole or substract some number as a whole, diff array is good

diff[i]: the supposed increase from i-1 to i

base: 
diff: +3 0 0 -3

信息论！！？以前我可能也知道但是不知道这么应用

i: delta = nums[i] - base
  increase [i:i+k-1] by delta
  diff[i]+=delta, diff[i+k]-=delta

i+1: base += diff[i]

okay.. so from the video, the base is just a number, it runs throough the array and greedily making the currect number at idx-i to comply

also yeah, it kind of seems I need to do it in reverse way..
base from 0 and increase to meet the numbers in nums
"""

class Solution:
    def checkArray(self, nums: List[int], k: int) -> bool:
        if k==1: return True
        n = len(nums)
        diff = [0]*n

        base = 0
        for i in range(n-1):
            # apply the diff so far
            base += diff[i]
            if base > nums[i]: return False
            delta = nums[i] - base 
            if i+k < n:
                diff[i] += delta 
                diff[i+k] -= delta
            # this step is to bring base to nums[i]
            base += delta
        
        return base+diff[n-1] == nums[n-1]
    
class Solution:
    def checkArray(self, nums: List[int], k: int) -> bool:
        if k==1: return True
        n = len(nums)
        diff = [0]*n

        base = 0
        for i in range(n-1):
            # apply the diff so far
            base += diff[i]
            if base > nums[i]: return False
            delta = nums[i] - base 
            diff[i] += delta 
            if i+k < n:
                diff[i+k] -= delta
            # this step is to bring base to nums[i]
            base += delta
        
        return base+diff[n-1] == nums[n-1]

class Solution:
    def checkArray(self, nums: List[int], k: int) -> bool:
        if k==1: return True
        n = len(nums)
        diff = [0]*n

        base = 0
        for i in range(n-1):
            # apply the diff so far
            base += diff[i]
            if base > nums[i]: return False
            delta = nums[i] - base 
            
            if i+k < n:
                diff[i+k] -= delta
            # this step is to bring base to nums[i]
            base += delta
        
        return base+diff[n-1] == nums[n-1]

"""
Runtime: 756 ms, faster than 98.08% of Python3 online submissions for Apply Operations to Make All Array Elements Equal to Zero.
Memory Usage: 31.1 MB, less than 56.26% of Python3 online submissions for Apply Operations to Make All Array Elements Equal to Zero.
"""

class Solution:
    def checkArray(self, nums: List[int], k: int) -> bool:
        if k==1: return True
        n = len(nums)
        diff = [0]*n
        base = [0]*n
        
        for i in range(n-1):
            if i:
              base[i] = diff[i] + base[i-1]
            if base[i] > nums[i]: return False
            delta = nums[i] - base[i]
            if i+k < n:
                diff[i+k] -= delta
            # this step is to bring base to nums[i]
            base[i] += delta
        
        return base[n-2]+diff[n-1] == nums[n-1]

"""
this is easier to understand
Runtime: 765 ms, faster than 98.02% of Python3 online submissions for Apply Operations to Make All Array Elements Equal to Zero.
Memory Usage: 31.3 MB, less than 22.47% of Python3 online submissions for Apply Operations to Make All Array Elements Equal to Zero.
"""

if __name__ == '__main__':
    s = Solution()

    # a = [0,16,0,29,0,0,0,9,0,0,0,0,0,0,0,0,0,95,49,0,0,0,0,68]
    # k = 24
    
    # print(s.checkArray(a,k))

    print(s.checkArray(nums = [2,2,3,1,1,0], k = 3))