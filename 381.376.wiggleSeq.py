"""
https://leetcode.com/problems/wiggle-subsequence/

okay.. without knowing this is a DP problem it will be probably very difficult
knowing it? 

so lets say dp[i] is the longest wiggleSeq ending at i

maybe also I keep two states
lastDiff is negative
lastDiff is positive

and depending on current diff.. 
positive... it can continue the lastDiff being negative.. 
negative... it can continue the lastDiff being positive..

if 0, both ends abruptly 

checking examples

the first two natrually form a seq if not equal 

         1, 7, 4, 9, 2, 5
neg   0  1  0  3  0  5  1
pos   0  1  2  2  4  2  6

7->4 -3, current diff is negative, so it can continue last positive seq, reaching 3
    what about positive? 1-4.. need to search backwards finding a smaller number???
    okay.. so maybe a positive seq is finding the first smaller number than myself.. then adding the negative seq len from it
    in the case of 4.. the first smaller is 1.. so it is 2? 

    taking one step back to 7
    last smaller is 1, and its negative seq len is 1(initial value)? so postive len at 7 is 2.. which is true 

    last bigger is not existent, so the neg seq len ending at 7 is 0... 

4->9 5, 
    finding last smaller to form postive, which is 4... so positive is 3+1->4
    finding last bigger number which is None, so cannot form a negtive diff here.. 

9->2, -7
    find last bigger number which is 9, can form negative from that positive seq, 4+1->5
    find last smaller number which is 1, can form postive from that neative seq, which will be 1+1->2

2->5, 3
    because it is positive diff, so naturally it can continue from 5's negative seq, which will be 5+1->6
    find last bigger which be 9, so forming negative seq from 9.. which will be 0+1->1

the thing now is clear.
two rows of states..

but also need to find the last bigger/smaller number index - maybe monotonic stack
"""


from functools import cache
from typing import List


class Solution_1st_trial_not_working:
    def wiggleMaxLength(self, nums: List[int]) -> int:

        # find last smaller/bigger num
        def lastSmaller():
            res = [-1] * len(nums)
            stack = []
            for i,num in enumerate(nums):
                while stack and stack[-1][1] > num:
                    stack.pop()
                if stack:
                    res[i] = stack[-1][0]
                else:
                    res[i] = -1
                stack.append([i,num])
            return res

        def lastBigger():
            res = [-1] * len(nums)
            stack = []
            for i,num in enumerate(nums):
                while stack and stack[-1][1] < num:
                    stack.pop()
                if stack:
                    res[i] = stack[-1][0]
                else:
                    res[i] = -1
                stack.append([i,num])
            return res
        
        leftSmallerIdxs = lastSmaller()
        lastBiggerIdxs = lastBigger()

        negSeq = [1] * len(nums) # the wiggle seq len ending at i and last diff is negative
        posSeq = [1] * len(nums) # the wiggle seq len ending at i and last diff is positive 

        res = 1
        for i,num in enumerate(nums):
            if i == 0 or (num - nums[i-1]==0):
                negSeq[i] = posSeq[i] = 1
                continue
                
            diff = num - nums[i-1]
            if diff > 0:
                posSeq[i] = negSeq[i-1] + 1
                # negSeq[i] = ?: finding last smaller, if it is >=0, then continue from there
                if lastBiggerIdxs[i] >=0:
                    negSeq[i] = posSeq[lastBiggerIdxs[i]] + 1
            else:
                negSeq[i] = posSeq[i-1] + 1
                if leftSmallerIdxs[i] >=0:
                    posSeq[i] = negSeq[leftSmallerIdxs[i]]+1
            res = max(res, posSeq[i], negSeq[i])
            print(f'after {i,num}')
            print('negtive:', negSeq)
            print('positive:', posSeq)
            print()
        return res

"""
a = [33, 53, 15, 21, 97, 8, 3, 43]

after (1, 53)
negtive: [1, 1, 1, 1, 1, 1, 1, 1]
positive: [1, 2, 1, 1, 1, 1, 1, 1]

after (2, 15)
negtive: [1, 1, 3, 1, 1, 1, 1, 1]
positive: [1, 2, 1, 1, 1, 1, 1, 1]

after (3, 21)
negtive: [1, 1, 3, 3, 1, 1, 1, 1]
positive: [1, 2, 1, 4, 1, 1, 1, 1]

after (4, 97)
negtive: [1, 1, 3, 3, 1, 1, 1, 1]
positive: [1, 2, 1, 4, 4, 1, 1, 1]

after (5, 8)
negtive: [1, 1, 3, 3, 1, 5, 1, 1]
positive: [1, 2, 1, 4, 4, 1, 1, 1]

after (6, 3)
negtive: [1, 1, 3, 3, 1, 5, 2, 1]
positive: [1, 2, 1, 4, 4, 1, 1, 1]

after (7, 43)
negtive: [1, 1, 3, 3, 1, 5, 2, 5]
positive: [1, 2, 1, 4, 4, 1, 1, 3]

5

wrong here!!!
43 can continue from 8's negative seq, which is 5.. so it can form 6

so maybe instead of looking at lastSmaller to form postive 
I look at lastBigger then one value to the right for the smaller

or maybe at 3.. I inheirt 5 instead of doing my own 
yeah... remove this number is also a valid choice
hum.. how to model that???
"""


class Solution_2nd_trial_not_working:
    def wiggleMaxLength(self, nums: List[int]) -> int:

        # find last smaller/bigger num
        def lastSmaller():
            res = [-1] * len(nums)
            stack = []
            for i, num in enumerate(nums):
                while stack and stack[-1][1] >= num:
                    stack.pop()
                if stack:
                    res[i] = stack[-1][0]
                else:
                    res[i] = -1
                stack.append([i, num])
            return res

        def lastBigger():
            res = [-1] * len(nums)
            stack = []
            for i, num in enumerate(nums):
                while stack and stack[-1][1] <= num:
                    stack.pop()
                if stack:
                    res[i] = stack[-1][0]
                else:
                    res[i] = -1
                stack.append([i, num])
            return res

        leftSmallerIdxs = lastSmaller()
        lastBiggerIdxs = lastBigger()

        print(leftSmallerIdxs)
        print(lastBiggerIdxs)

        # the wiggle seq len ending at i and last diff is negative
        negSeq = [1] * len(nums)
        # the wiggle seq len ending at i and last diff is positive
        posSeq = [1] * len(nums)

        res = 1
        for i, num in enumerate(nums):
            if i == 0:
                negSeq[i] = posSeq[i] = 1
                continue

            diff = num - nums[i-1]
            if diff > 0:
                posSeq[i] = max(negSeq[i-1] + 1, posSeq[i-1])
                # negSeq[i] = ?: finding last smaller, if it is >=0, then continue from there
                if lastBiggerIdxs[i] >= 0:
                    biggerIdx = lastBiggerIdxs[i]
                    smallerIdx = leftSmallerIdxs[i]
                    while biggerIdx>smallerIdx:
                        if nums[biggerIdx] > num:
                            negSeq[i] = max(negSeq[i], posSeq[biggerIdx] + 1)
                        biggerIdx -= 1

            if diff < 0:
                negSeq[i] = max(posSeq[i-1] + 1, negSeq[i-1])
                if leftSmallerIdxs[i] >= 0:
                    biggerIdx = lastBiggerIdxs[i]
                    smallerIdx = leftSmallerIdxs[i]
                    while smallerIdx > biggerIdx:
                        if nums[smallerIdx] < num:
                            posSeq[i] = max(posSeq[i], negSeq[smallerIdx]+1)
                        smallerIdx-=1 

                    
            res = max(res, posSeq[i], negSeq[i])
            print(f'after {i,num}')
            print('negtive:', negSeq)
            print('positive:', posSeq)
            print()

        return res

"""
okay.. don't think I can crack it tonight
I maybe should try recursive first 

or maybe there should be a thrid row.. not choose myself...

f(i, lastNum) 
    choices
        increasing nums[i] > lastNum
        decreasing nums[i] < lastNum
        skip...

"""


class Solution:
    def wiggleMaxLength(self, nums: List[int]) -> int:

        @cache
        def f(idx, lastNum, posSeq, negSeq):
            if idx >= len(nums):
                return max(posSeq, negSeq)

            diff = nums[idx] - lastNum
            res = 1
            if diff > 0:
                # I can continue from negSeq
                res = max(res, f(idx+1, nums[idx], negSeq+1, negSeq))
            elif diff < 0:
                # I can contninue from posSeq
                res = max(res, f(idx+1, nums[idx], posSeq, posSeq+1))
            else:
                # I can skip myself
                res = max(res, f(idx+1, lastNum, posSeq, negSeq))
            return res

        return f(1, nums[0], 1, 1)

"""
okay.. so much fuck
I must have thought too complicated...

Runtime: 36 ms, faster than 88.48% of Python3 online submissions for Wiggle Subsequence.
Memory Usage: 14.9 MB, less than 5.03% of Python3 online submissions for Wiggle Subsequence.

I was even thinking I need to skip the first element... 
you don't...
so there is a greedy tag 


okay my biggest confusion here is 
ending at idx means:
    up to idx       <- this is the right meaning here
    including idx   <- this is what I was trying to model...
"""

if __name__ == '__main__':
    

    # print(Solution().wiggleMaxLength([1,7,4,9,2,5]))
    # print(Solution().wiggleMaxLength(
    #     [1, 2, 3, 4, 5, 6, 17, 5, 10, 13, 15, 10, 5, 16, 8]))
    # print(Solution().wiggleMaxLength([1,2,3,4,5,6,7,8,9]))

    a = [33, 53, 15, 21, 97, 8, 3, 43]
    # a = [0,0]
    a = [1, 7, 4, 9, 2, 5]
    print(Solution().wiggleMaxLength(a))
