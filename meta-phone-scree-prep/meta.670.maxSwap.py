from collections import defaultdict
from typing import Counter


class Solution:
    def maximumSwap(self, num: int) -> int:
        numIdxes = defaultdict(list)
        nums = []
        idx = 0
        
        while num:
            digit = num%10
            numIdxes[digit].append(idx)
            nums.append(digit)
            num//=10
            idx += 1
        
        maxDigit = max(numIdxes.keys())

        # find the swap position
        i = len(nums)-1
        frontMax = 0
        while i>=0 and nums[i] == maxDigit:
            frontMax += 1
            i-=1

        idxLastMaxDigit = numIdxes[maxDigit][-1]
        if i>=0 and len(numIdxes[maxDigit])>frontMax:
            nums[i], nums[idxLastMaxDigit] = nums[idxLastMaxDigit], nums[i]
        
        res = 0
        nums.reverse()
        for num in nums:
            res = res*10 + num
        
        return res
  
"""
ugh.. I only thought about the max digit, but it could be 2nd or 3rd max to be swapped
this is not very easy

so I should always do more example study before diving in
so I can sort it

9 8 3 6 8
9 8 8 6 3

find first different num

2 7 3 6
7 6 3 2

9973
9973


"""
class Solution:
    def maximumSwap(self, num: int) -> int:
        nums = []
        while num:
            digit = num%10
            nums.append(digit)
            num//=10

        copy = list(nums)
        copy.sort()
        copy.reverse()
        nums.reverse()

        for idx, (n,c) in enumerate(zip(nums,copy)):
            if n!=c:
                # minNum to swap is n
                # bigNum to swap is c
                # just need to scap from behind to find bigNum
                break 
        for j in range(len(nums)-1, idx, -1):
            if nums[j] == c:
                nums[idx], nums[j] = nums[j], nums[idx]
                break
        res = 0
        for num in nums:
            res = res*10 + num
        
        return res

                        





if __name__ == '__main__':
    s = Solution()
    print(s.maximumSwap(2736))
