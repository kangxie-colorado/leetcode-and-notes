"""
https://leetcode.com/problems/count-of-range-sum/

bi-tree??? no idea... 
I cannot figure out this myself.. 

I watched the video and got the idea 
so I am just now trying to implement the idea

a divide and conquer solution 
left, right, and cross...

the cross being the tricky part..
this can also be used in that maxSubarry problem

but kind of more tricky 
"""


import bisect
from typing import List


class Solution:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        # 1. calculate the prefix sum - O(n)
        # we need to translate this problem into finding the pair-(i,j)
        # sum(i,j) = sum(j) - sum(i-1)
        # e.g. the sum(1,1) = sums[1] - sums[0] -> the sum of first element 
        # sum(1,3) = sums[3] - sums[0] -> the sum of first 3 elements 
        sums = [0] * (len(nums)+1)
        for i,n in enumerate(nums):
            sums[i+1] = sums[i] + n

        # 2. in that sums array, we search pairs of i,j where
        #  sum(i,j) in [lower, upper]
        #  or say  lower <= sums[j] - sums[i-1] <= upper 
        #  two variables make it pretty difficult to reason about so transform
        #  fix i, finding j where sums[i-1] + lower <= sums[j] <= sums[i-1] + upper 
        # notice this is logicall i-1 and j pair, but a pair of (i-1,j) is just a pair of (i,j)
        # let me see 
        def pairs(i,j):
            if i>j:
                return 0 
            if i == j:
                return 1 if  lower<= sums[j] - sums[i-1]<=upper else 0
            
            m = i+(j-i)//2
            # divide and conquer 
            leftPairs = pairs(i,m)
            rightPairs = pairs(m+1,j)

            # cross over the m
            # fix left side, finding the range in the right side that fits sums[i-1] + lower <= sums[j] <= sums[i-1] + upper
            # sums[i-1] + lower <= sums[j] <= sums[i-1] + upper
            crossPairs = 0
            for l in range(i,m+1):
                # searching for upper-bound? lower-bound? of sums[l-1]+upper
                # yeah, upper bound.. the first number that is > "sums[l-1]+upper"
                y = bisect.bisect_right(sums[m+1:j+1], sums[l-1]+upper)
                # searching for lower-bound
                x = bisect.bisect_left(sums[m+1:j+1], sums[l-1]+lower)
                crossPairs += y-x
            
            # so that merge sort naturally has some relationship to divide and conquer
            # and here we need to borrow the idea of merge sort
            # before return we need to sort 
            temp = []
            left = sums[i:m+1]
            right = sums[m+1:j+1]

            l=r=0
            while l<len(left) and r<len(right):
                if left[l] < right[r]:
                    temp.append(left[l])
                    l+=1
                else:
                    temp.append(right[r])
                    r+=1
            temp.extend(left[l:] or right[r:])
            sums[i:j+1] = temp
            return leftPairs + crossPairs + rightPairs

        return pairs(1,len(nums))

"""
61 / 67 test cases passed.


TLE...
"""


class Solution:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        # 1. calculate the prefix sum - O(n)
        # we need to translate this problem into finding the pair-(i,j)
        # sum(i,j) = sum(j) - sum(i-1)
        # e.g. the sum(1,1) = sums[1] - sums[0] -> the sum of first element
        # sum(1,3) = sums[3] - sums[0] -> the sum of first 3 elements
        sums = [0] * (len(nums)+1)
        for i, n in enumerate(nums):
            sums[i+1] = sums[i] + n

        # 2. in that sums array, we search pairs of i,j where
        #  sum(i,j) in [lower, upper]
        #  or say  lower <= sums[j] - sums[i-1] <= upper
        #  two variables make it pretty difficult to reason about so transform
        #  fix i, finding j where sums[i-1] + lower <= sums[j] <= sums[i-1] + upper
        # notice this is logicall i-1 and j pair, but a pair of (i-1,j) is just a pair of (i,j)
        # let me see
        def pairs(i, j):
            if i > j:
                return 0
            if i == j:
                return 1 if lower <= sums[j] - sums[i-1] <= upper else 0

            m = i+(j-i)//2
            # divide and conquer
            leftPairs = pairs(i, m)
            rightPairs = pairs(m+1, j)

            # cross over the m
            # fix left side, finding the range in the right side that fits sums[i-1] + lower <= sums[j] <= sums[i-1] + upper
            # sums[i-1] + lower <= sums[j] <= sums[i-1] + upper
            crossPairs = 0
            for l in range(i, m+1):
                # searching for upper-bound? lower-bound? of sums[l-1]+upper
                # yeah, upper bound.. the first number that is > "sums[l-1]+upper"
                y = bisect.bisect_right(sums, sums[l-1]+upper, lo=m+1, hi=j+1) - (m+1)
                # searching for lower-bound
                x = bisect.bisect_left(sums, sums[l-1]+lower, lo=m+1, hi=j+1) - (m+1)
                # no need to -(m+1) because both do the same
                crossPairs += y-x

            # so that merge sort naturally has some relationship to divide and conquer
            # and here we need to borrow the idea of merge sort
            # before return we need to sort
            # temp = []
            # l, r = i,m+1
            # while l < m+1 and r < j+1:
            #     if sums[l] < sums[r]:
            #         temp.append(sums[l])
            #         l += 1
            #     else:
            #         temp.append(sums[r])
            #         r += 1
            # if l<m+1:
            #     temp.extend(sums[l:m+1])
            # else:
            #     temp.extend(sums[r:j+1])
            # sums[i:j+1] = temp

            sums = sums[:i] + sorted(sums[i:j+1]) + sums[j+1:]

            return leftPairs + crossPairs + rightPairs

        return pairs(1, len(nums))


class Solution:
    def countRangeSum(self, nums, lower, upper):
        n = len(nums)
        #  BITree stores how many elements rank <= me so far
        Sum, BITree = [0] * (n + 1), [0] * (n + 2)

        def count(x):
            s = 0
            while x:
                s += BITree[x]
                x -= (x & -x)
            return s

        def update(x):
            while x <= n + 1:
                BITree[x] += 1
                x += (x & -x)

        for i in range(n):
            Sum[i + 1] = Sum[i] + nums[i]
        sortSum, res = sorted(Sum), 0
        print(f"Sum: {Sum}; sortSum: {sortSum}")
        print()
        for sum_j in Sum:
            print(f'checking sum_j:{sum_j}; BITree {BITree};')
            
            rankHigh = bisect.bisect_right(sortSum, sum_j - lower)
            rankLow = bisect.bisect_left(sortSum, sum_j - upper)
            print(f"checking {sum_j - lower, sum_j - upper}, their ranks: "f"{rankHigh}, {rankLow}")

            highRankCount = count(rankHigh) 
            lowRankCount = count(rankLow)
            print(
                f"{highRankCount} range sums <= {rankHigh}; {lowRankCount} range sums <= {rankLow}; the diff is the sum_i_count")
            sum_i_count = highRankCount - lowRankCount
            res += sum_i_count
            print(f"between rank{rankHigh} and rank{rankLow}, {sum_i_count} paris are kept in BITree and res is {res}")

            update(bisect.bisect_left(sortSum, sum_j) + 1)
            print(
                f"After update sum_j(rank: {bisect.bisect_left(sortSum, sum_j)+1}) , BITree {BITree}")
            print()
        return res


"""
less array copy logic 
Runtime: 5599 ms, faster than 47.54% of Python3 online submissions for Count of Range Sum.
Memory Usage: 48.1 MB, less than 27.16% of Python3 online submissions for Count of Range Sum.


that BITree solution is really hard to understand 

I printed out a lot of information on this example

# Sum: [0, -2, 3, 2]; sortSum: [-2, 0, 2, 3]

# checking sum_j:0; BITree [0, 0, 0, 0, 0];
# checking (2, -2), their ranks: 3, 0
# 0 range sums <= 3; 0 range sums <= 0; the diff is the sum_i_count
# between rank3 and rank0, 0 paris are kept in BITree and res is 0
# After update sum_j(rank: 2) , BITree [0, 0, 1, 0, 1]

# checking sum_j:-2; BITree [0, 0, 1, 0, 1];
# checking (0, -4), their ranks: 2, 0
# 1 range sums <= 2; 0 range sums <= 0; the diff is the sum_i_count
# between rank2 and rank0, 1 paris are kept in BITree and res is 1
# After update sum_j(rank: 1) , BITree [0, 1, 2, 0, 2]

# checking sum_j:3; BITree [0, 1, 2, 0, 2];
# checking (5, 1), their ranks: 4, 2
# 2 range sums <= 4; 2 range sums <= 2; the diff is the sum_i_count
# between rank4 and rank2, 0 paris are kept in BITree and res is 1
# After update sum_j(rank: 4) , BITree [0, 1, 2, 0, 3]

# checking sum_j:2; BITree [0, 1, 2, 0, 3];
# checking (4, 0), their ranks: 4, 1
# 3 range sums <= 4; 1 range sums <= 1; the diff is the sum_i_count
# between rank4 and rank1, 2 paris are kept in BITree and res is 3
# After update sum_j(rank: 3) , BITree [0, 1, 2, 1, 4]

# 3

my mind is too tired today to work this out
reserve for future learning

https://leetcode.com/problems/count-of-range-sum/discuss/77986/O(NlogN)-Python-solution-binary-indexed-tree-268-ms
^ this only works on fixing j to search i

https://leetcode.com/problems/count-of-range-sum/discuss/78026/An-O(n-log-n)-solution-via-Fenwick-Tree
this works fixing i to serach j... 

their update/query orders are different 
not sure 


"""


class Solution_NotWorking:
    def countRangeSum(self, nums, lower, upper):
        n = len(nums)
        #  BITree stores how many elements rank <= me so far
        Sum, BITree = [0] * (n + 1), [0] * (n + 2)

        def count(x):
            s = 0
            while x:
                s += BITree[x]
                x -= (x & -x)
            return s

        def update(x):
            while x <= n + 1:
                BITree[x] += 1
                x += (x & -x)

        for i in range(n):
            Sum[i + 1] = Sum[i] + nums[i]
        sortSum, res = sorted(Sum), 0
        print(f"Sum: {Sum}; sortSum: {sortSum}")
        print()
        for sum_i in Sum:
            print(f'checking sum_i:{sum_i}; BITree {BITree};')

            rankHigh = bisect.bisect_right(sortSum, sum_i + upper)
            rankLow = bisect.bisect_left(sortSum, sum_i + lower)
            print(
                f"checking { sum_i + upper, sum_i + lower}, their ranks: "f"{rankHigh}, {rankLow}")

            highRankCount = count(rankHigh)
            lowRankCount = count(rankLow)
            print(
                f"{highRankCount} range sums <= {rankHigh}; {lowRankCount} range sums <= {rankLow}; the diff is the sum_j_count")
            sum_j_count = highRankCount - lowRankCount
            res += sum_j_count
            print(
                f"between rank{rankHigh} and rank{rankLow}, {sum_j_count} paris are kept in BITree and res is {res}")

            update(bisect.bisect_left(sortSum, sum_i) + 1)
            print(
                f"After update sum_i(rank: {bisect.bisect_left(sortSum, sum_i)+1}) , BITree {BITree}")
            print()
        return res

"""
Sum: [0, 2147483647, -1, -2, -2]; sortSum: [-2, -2, -1, 0, 2147483647]

checking sum_i:0; BITree [0, 0, 0, 0, 0, 0];
checking (0, -1), their ranks: 4, 2
0 range sums <= 4; 0 range sums <= 2; the diff is the sum_j_count
between rank4 and rank2, 0 paris are kept in BITree and res is 0
After update sum_i(rank: 4) , BITree [0, 0, 0, 0, 1, 0]

checking sum_i:2147483647; BITree [0, 0, 0, 0, 1, 0];
checking (2147483647, 2147483646), their ranks: 5, 4
1 range sums <= 5; 1 range sums <= 4; the diff is the sum_j_count
between rank5 and rank4, 0 paris are kept in BITree and res is 0
After update sum_i(rank: 5) , BITree [0, 0, 0, 0, 1, 1]

checking sum_i:-1; BITree [0, 0, 0, 0, 1, 1];
checking (-1, -2), their ranks: 3, 0
0 range sums <= 3; 0 range sums <= 0; the diff is the sum_j_count
between rank3 and rank0, 0 paris are kept in BITree and res is 0
After update sum_i(rank: 3) , BITree [0, 0, 0, 1, 2, 1]

checking sum_i:-2; BITree [0, 0, 0, 1, 2, 1];
checking (-2, -3), their ranks: 2, 0
0 range sums <= 2; 0 range sums <= 0; the diff is the sum_j_count
between rank2 and rank0, 0 paris are kept in BITree and res is 0
After update sum_i(rank: 1) , BITree [0, 1, 1, 1, 3, 1]

checking sum_i:-2; BITree [0, 1, 1, 1, 3, 1];
checking (-2, -3), their ranks: 2, 0
1 range sums <= 2; 0 range sums <= 0; the diff is the sum_j_count
between rank2 and rank0, 1 paris are kept in BITree and res is 1
After update sum_i(rank: 1) , BITree [0, 2, 2, 1, 4, 1]

1

from this, kind of feel why it doesn't work for fixing i to search j

checking sum_i:-1; BITree [0, 0, 0, 0, 1, 1];
checking (-1, -2), their ranks: 3, 0
0 range sums <= 3; 0 range sums <= 0; the diff is the sum_j_count
between rank3 and rank0, 0 paris are kept in BITree and res is 0
After update sum_i(rank: 3) , BITree [0, 0, 0, 1, 2, 1]

vs 

(fixing j first)
checking sum_j:-1; BITree [0, 0, 0, 0, 1, 1];
checking (0, -1), their ranks: 4, 2
1 range sums <= 4; 0 range sums <= 2; the diff is the sum_i_count
between rank4 and rank2, 1 paris are kept in BITree and res is 1
After update sum_j(rank: 3) , BITree [0, 0, 0, 1, 2, 1]

kind of.. 
you are doing left to right.. 
put each sum into the tree... what is put into the tree
their ranking information

if idx-1 ranks 1st (smallest), then <=1 will be 1, <=2 will be 1, <=4 will be 1
so it kind of feel like ending at sum_j... 

if you do sum_i... probably need to reverse something 
no idea.. 

I need to stop now.. tomorrow needs me

"""




if __name__ == '__main__':
    S = Solution()
    # print(S.countRangeSum([-2,5,-1], -2, 2))
    print(S.countRangeSum([2147483647, -2147483648, -1, 0], -1, 0))
