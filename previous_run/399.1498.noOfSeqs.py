"""
https://leetcode.com/problems/number-of-subsequences-that-satisfy-the-given-sum-condition/

I first thought of sorting
then I rejected that idea.. because it could change the order of elements

then I see the in the tags sorting is indeed there.. 
so I come back to think it again

what if I keep the index with it..
then I can find fix a min.. search a max... or fix a max.. search a min?

[3,5,6,7] target = 9
after sorting: (3,0) (5,1) (6,2) (7,3)

with 3.. I search 1 to 6, because element is positve and it can add up to 6 to 3 and still <= 9
3: search 1.. 0.. how many? 
3: search 2.. 
3: search 3.. 0.. how many? 0-0+1 = 1? if so, what about above... so I think search bisect_right 
3: search 4.. 1.. how many? 4 is not in there... 

so maybe.. no need to search 1/2/4..

just fix at 3.. itself... 
and next... next what? next number or next index???

but 3 6 5 is the same as 3 5 6... 
sounds like I should fix two pointers.. 

fix a min and fix a max... see.. how many can be included 
fix 3, fix 7.. not possible 7->6
    3 5 6... how many? [3,6] [3,5,6]
    now walk 6, 6->5.. because 6+6>9 (itself)
    3,4.. how many [3,5]
    now because 5+5>9, walk 5 ->3
    3 how many [3]

happend to be right but check another one

nums = [3,3,6,8], target = 10
sorting (3,0) (3,1) (6,2) (8,3)
3 8.. no way.. 8->6
    3 6.. it is idx-0 and idx-2.. therefore it is 3 X 6, how many [3 x 6] [3 6]
    6+6 > 10, 6-3
    3 3... [3,3]
    now.. I am lost.. 
    so this is not the right way

think more time.. 
at long as I fix a min and max.. the middle number i don't care where they 
1 6 X Y Z -> [1,6] [1,6,X] [1,6,Y] [1,6,Z] [1,6,X,Y,Z] [1,6,X,Y]
the same goese with 1 X Y Z 6

so now the problem becomes a bit clear
fix i, fix j.. where A[i] + A[j] <= target 
then search how many k where A[i] <= A[k] <= A[j]

nums = [3,3,6,8], target = 10
after sorting it is the same

3vs8.. not possible
3vs6 search bisect_left(3)->0, bisect_right(6),3 .. excluding 3 and 6 themselves.. there are 1 number in between that makes 2.. taking the middle 3 or not
now where to move.. 

also... we know for any X in between [3, X, 6] 3<=X<=6.. so for any X, [3,X] [X,6] it will be ok.. 1 + anything in between this will give me another 2.. 
then 3 and 6 itself... 3 can do.. 

but I still missing the middle 3... so maybe I don't think that much .. just calculate per each element and see

give 3... search 7... bisect_left(7)->3 meaning idx-0 to idx-3 (depending on equal to 7 or not)



    

"""


import bisect
from typing import List


class Solution:
    def numSubseq(self, nums: List[int], target: int) -> int:
        mod = 10**9+7
        nums.sort()
        res = 0
        for i, num in enumerate(nums):
            if num > target:
                break

            if num*2 <= target:
                res += 1

            otherNum = target-num
            idx = bisect.bisect_right(nums, otherNum)
            # idx-i: the len of the widow
            # 2: the start and end element
            midNumbers = idx-i-2
            while midNumbers >= 0:
                # why using while
                # e.g. 3,5,6.. min/max being 3/6 can do
                # 3/5 can also do...
                res += 1<<midNumbers
                res %= mod
                midNumbers -= 1
        return res

"""
50 / 62 test cases passed.
and TLE

hum... 
2**midNumbers.. 1<<num + 1<<(num-1)...
basically is 1<<(num+1)-1
"""


class Solution:
    def numSubseq(self, nums: List[int], target: int) -> int:
        mod = 10**9+7
        nums.sort()
        res = 0
        for i, num in enumerate(nums):
            if num > target:
                break

            if num*2 <= target:
                res += 1

            otherNum = target-num
            idx = bisect.bisect_right(nums, otherNum)
            # idx-i: the len of the widow
            # 2: the start and end element
            midNumbers = idx-i-2
            if midNumbers >= 0:
                # why using while
                # e.g. 3,5,6.. min/max being 3/6 can do
                # 3/5 can also do...
                incr = 1<<(midNumbers+1)
                res += incr-1
                res %= mod
        return res

"""
Runtime: 2487 ms, faster than 39.16% of Python3 online submissions for Number of Subsequences That Satisfy the Given Sum Condition.
Memory Usage: 26.8 MB, less than 78.29% of Python3 online submissions for Number of Subsequences That Satisfy the Given Sum Condition.

okay.. there is actually a two pointers solution again
"""


class Solution:
    def numSubseq(self, nums: List[int], target: int) -> int:
        mod = 10**9+7
        nums.sort()
        res = 0

        i,j=0,len(nums)-1
        while i<=j:
            if nums[i] + nums[j] > target:
                j-=1
            else:
                res += pow(2, j-i, mod)
                i+=1
        return res % mod

"""
Runtime: 837 ms, faster than 91.58% of Python3 online submissions for Number of Subsequences That Satisfy the Given Sum Condition.
Memory Usage: 26.7 MB, less than 96.92% of Python3 online submissions for Number of Subsequences That Satisfy the Given Sum Condition.

like TWO SUM.. sorted array...
also this is what the hints are about..

for any i, find the max j -- it is in the else: part; if the sum <= target.. then this j is max-j for that i; count and move on

"""


if __name__ == '__main__':
    s =Solution()
    print(s.numSubseq(nums=[3, 5, 6, 7], target=9))
    print(s.numSubseq(nums=[3, 3, 6, 8], target=10))
    print(s.numSubseq(nums=[2, 3, 3, 4, 6, 7], target=12))

