"""
https://leetcode.com/problems/maximum-number-of-consecutive-values-you-can-make/?envType=study-plan&id=programming-skills-iii

let me do brute force first???
"""


from collections import Counter, defaultdict
from typing import List

from sortedcontainers import SortedList


class Solution:
    def getMaximumConsecutive(self, coins: List[int]) -> int:
        C = defaultdict(int)
        S = 0
        for c in coins:
            C[c] += 1
            S += c

        dp = [0]*(S+1)
        dp[0] = 1
        C[0] = 1

        for i in range(1, S+1):

            for j in range(0, j):
                if dp[i] and j-i in C:
                    dp[j] = True

        return None


"""

no way thru:
but looking at example 3 gives me an insight
Input: nums = [1,4,10,3,1]
Output: 20

[1,1,3,4] could form 0-9
then plus 10.. it could form 10-19

then I think might I just need sort and form
[1] -> set(0,1)
one more 1[..., 1] -> [1,2] -> set(0,1,2)
one more 3 -> (3,4,5) -> set(0,1,2,3,4,5)
one more 4-> set(0,1,2,3,4,5,6,7,8,9)
...

if there is a break point.. then we can stop... or until we used up all numbers 


I even thought backtrack.. but apparently backtrack cannot solve this big input
"""


class Solution:
    def getMaximumConsecutive(self, coins: List[int]) -> int:
        valSL = SortedList([0])
        valSet = {0}

        coins.sort()
        for c in coins:
            toAdd = set()
            oldMax = valSL[-1]
            for n in valSL:
                if n+c > oldMax+1:
                    break
                if n+c not in valSet:
                    oldMax = max(oldMax, n+c)
                    toAdd.add(n+c)

            for n in toAdd:
                valSL.add(n)
                valSet.add(n)

        return len(valSet)


"""
27 / 72 test cases passed.

hmm.. 
okay.. there is at least one attribute I am not paying attention 
the valSL is already fully filled 

the new n comes.. it can make to n+min,n+max
if n+min>max+1, then whoops... otherwise, the range just becomes [0,n+max]

so yeah.. I just two end points
"""


class Solution:
    def getMaximumConsecutive(self, coins: List[int]) -> int:

        end = 0
        coins.sort()
        for c in coins:
            if c > end+1:
                break
            end += c
        return end+1


"""
Runtime: 765 ms, faster than 97.67% of Python3 online submissions for Maximum Number of Consecutive Values You Can Make.
Memory Usage: 19.7 MB, less than 45.93% of Python3 online submissions for Maximum Number of Consecutive Values You Can Make.
"""


if __name__ == '__main__':
    s = Solution()
    A = [56, 684, 91, 1, 843, 135, 1, 870, 614, 1, 912, 726, 1, 293, 444, 1, 1, 35, 1, 1, 1, 1, 657, 1, 551, 66, 834, 1, 1, 507, 268, 560, 1, 15, 795, 60, 367, 1000, 1, 135, 929, 1, 147, 1, 1, 1, 619, 639, 1, 24, 915, 441, 833, 1, 1, 503, 1, 1, 196, 471, 1, 374, 309, 1, 450, 1, 78, 541, 1, 1, 877, 329, 1, 750, 382, 33, 165, 318, 1, 510, 1, 1, 492, 695, 313, 1, 309, 1, 1, 175, 1, 618, 1, 1, 1, 1, 190, 288, 1, 1, 1, 545, 1, 1, 838, 1, 370, 1, 1, 1, 1, 519, 798, 38, 1, 1, 843, 503, 514, 1, 990, 1, 1, 1, 1, 874, 22, 1, 557, 225, 1, 1, 443, 1, 128, 810, 667, 287, 1, 1, 1, 546, 1, 1, 1, 945, 1, 1, 1, 1, 1, 1, 1, 675, 188, 1, 1, 267, 1, 883, 1, 696, 1, 919, 1, 1, 215, 1, 1, 148, 1, 514, 1, 1, 171, 306, 1, 1, 742, 1, 1, 1, 721, 211, 1, 1, 1, 12, 175, 1, 760, 1, 1, 1, 1, 1, 1, 1, 1, 298, 1, 299, 1, 182, 932, 1, 696, 611, 91, 381, 647, 1, 1, 270, 667, 664, 1, 1, 186, 620, 965, 1, 1, 1, 1, 1, 950, 1, 824, 1, 1, 1, 1, 1, 546, 186, 1, 1, 934, 446, 1, 1, 1, 1, 411, 1, 1, 1, 1, 1, 792, 755, 129, 974, 1, 1, 1, 1,
         427, 123, 317, 240, 1, 1, 702, 563, 930, 1, 1, 308, 403, 86, 1, 1, 1, 1, 1, 780, 1, 171, 891, 526, 221, 1, 913, 949, 1, 866, 1, 6, 1, 383, 690, 1, 1, 1, 609, 635, 1, 729, 1, 1, 1, 1, 645, 1, 187, 1, 990, 1, 840, 813, 1, 1, 873, 571, 689, 1, 88, 1, 109, 1, 1, 1, 787, 64, 266, 415, 1, 1, 1, 1, 1, 99, 653, 1, 1, 532, 366, 73, 1, 94, 302, 824, 113, 67, 651, 551, 274, 1, 236, 1, 1, 1, 874, 400, 863, 638, 1, 624, 1, 1, 42, 1, 1, 431, 1, 508, 782, 755, 423, 1, 486, 855, 387, 1, 1, 993, 1, 1, 645, 1, 28, 151, 1, 1, 1, 1, 1, 753, 535, 1, 186, 146, 1, 1, 629, 148, 1, 340, 857, 543, 1, 1, 1, 1, 1, 927, 470, 1, 1, 777, 90, 928, 1, 329, 1, 1, 256, 1, 1, 352, 26, 1, 556, 1, 305, 874, 1, 218, 424, 1, 103, 261, 670, 1, 1, 711, 599, 396, 1, 411, 1, 645, 1, 1, 1, 908, 1, 573, 728, 1, 1, 793, 1, 297, 1, 1, 843, 78, 894, 1, 16, 1, 525, 1000, 213, 366, 291, 549, 1, 258, 1, 172, 1, 840, 1, 1, 863, 1, 924, 679, 1, 1, 1, 420, 542, 932, 548, 449, 962, 1, 1, 1, 1, 522, 858, 1, 1, 1, 147, 1, 1, 1, 11, 591, 1, 1, 1, 578]
    print(s.getMaximumConsecutive(A))
