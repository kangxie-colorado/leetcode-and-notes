"""
first I thought this is a sliding window
but then I saw the negative number.. it cannot be that simple

so this should be a prefixSum kind issue

"""

import bisect
from collections import defaultdict
from typing import List


class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        prefixSums = [0]*(n+1)
        res = 0

        for i in range(1,n+1):
            prefixSums[i] = nums[i-1] + prefixSums[i-1]
          
        # because of negative, pSum can go up and down, no binary search
        # but idx only grows one direction, can do search
        sumIdxMap = defaultdict(list)
        for idx,psum in enumerate(prefixSums):
            sumIdxMap[psum].append(idx)
        
        for pSum1 in sumIdxMap:
            pSum2 = pSum1 + k
            if pSum2 in sumIdxMap:
                idxes_1 = sumIdxMap[pSum1]
                idxes_2 = sumIdxMap[pSum2]

                # for each idx-1, finding its insert position in idxes-2 
                # then the eligible idxes-2 are len(idxes-2) - bst_pos?
                for idx1 in idxes_1:
                    # A TRICK here, this needs to be right
                    # to deal with sum-0, hard to explain.. let me think about this later
                    # this thing is once I used bisect_right, it passed
                    pos = bisect.bisect_right(idxes_2, idx1)
                    res += len(idxes_2)-pos
        
        return res

"""
so this worked but I don't know exactly how, that pos and len() - pos part are kind of lucky guess
but this was solved before and it is a pathSum problem

let me try coming up with that again
"""

class Solution(object):
    def subarraySum(self, nums, k):
        pathSumMap = defaultdict(int)
        preSum = 0
        # we need to initialize count of sum-0 to 1
        # e.g. [1,2,3], k=1, the first element will be meeting the k already
        # actually maybe I could generilize this with an extra element
        pathSumMap[0] = 1 
        res = 0

        for idx,num in enumerate(nums):
            # this is my current pathSum up to idx
            # it will be preSum + my current number
            nums[idx] += preSum
            res += pathSumMap[nums[idx]-k]

            preSum = nums[idx]
            pathSumMap[nums[idx]] += 1
        
        return res

class Solution(object):
    def subarraySum(self, nums, k):
        n = len(nums)
        prefixSums = [0] * (n+1)

        for i in range(1, n+1):
            prefixSums[i] = prefixSums[i-1] + nums[i-1]
        
        pathSumMap = defaultdict(int)
        res = 0
        for idx,pSum in enumerate(prefixSums):
            res += pathSumMap[pSum-k]
            pathSumMap[pSum] += 1
        return res

"""
Runtime: 286 ms, faster than 88.33% of Python3 online submissions for Subarray Sum Equals K.
Memory Usage: 20.9 MB, less than 6.29% of Python3 online submissions for Subarray Sum Equals K.
"""

if __name__ == '__main__':
    s = Solution()

    print(s.subarraySum(nums = [1], k = 0))