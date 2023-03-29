"""
https://leetcode.com/problems/handshakes-that-dont-cross/

interesting
I think this could be converted to pairs finding?

when do we have a cross?
1-3 2-4, the pair overlap and not fully contain
other cases
1-2 3-4, non-overlap 
1-4 2-3, fully contain 

it might have some math property?
for n=2 to n=18

1
2
5
14
42
132
429
1430
4862

it does seem to be some math property 

so this is how I look at it
this gives 2 as we know
1 2
4 3

adding 5 and 6
6 1 2 
5 4 3

now we can focus on 6
6 with 1: between there are 0 numbers and 4 numbers, can form, and we know 4 group gives 2
6 with 2: between there are 1 and 3 numbers, cannot form, 0
6 with 3: between there are 2 and 2 numbers, can form and we know 2 is 1, 1*1 is 1
(we can initiate dp[0] = 1)
6 with 4: between there are 3 and 1 numbers, cannot form, 0
6 with 5: between there are 4 and 0 numbers, can form, 2

2+1+2 =? 5

now adding 7 and 8

7 8 1 2
6 5 4 3

8 with 1: 0 and 6, 1*5=5
8 with 2: 0
8 with 3: 2 and 4: 1*2=2
8 with 4: 0
8 with 5: 2 and 4, 1*2 = 2 
8 with 6: 0
8 with 7: 0 and 6: 1*5=5
5+5+2+2 = 14

think I can give a try already

"""


class Solution:
    def numberOfWays(self, numPeople: int) -> int:

        dp = [0] * (numPeople+1)
        dp[0] = dp[2] = 1
        mod = 10**9+7

        for i in range(4,numPeople+1,2):
            for j in range(1,i):
                # what are the number of elements in each half
                num1 = j-1
                num2 = i-2-num1 

                dp[i] += dp[num1]*dp[num2]
                dp[i] %= mod
                
        
        return dp[numPeople]


class Solution:
    def numberOfWays(self, numPeople: int) -> int:

        dp = [0] * (numPeople+1)
        dp[0] = dp[2] = 1
        mod = 10**9+7

        for i in range(4, numPeople+1, 2):
            for j in range(1, i, 2): # step in 2
                # what are the number of elements in each half
                num1 = j-1
                num2 = i-2-num1

                dp[i] += dp[num1]*dp[num2]
                dp[i] %= mod

        return dp[numPeople]

"""
Runtime: 659 ms, faster than 52.04% of Python3 online submissions for Handshakes That Don't Cross.
Memory Usage: 13.8 MB, less than 73.47% of Python3 online submissions for Handshakes That Don't Cross.


step in 2 improves to this
"""

if __name__ == '__main__':
    s = Solution()
    print(s.numberOfWays(4))
    print(s.numberOfWays(6))
    print(s.numberOfWays(8))
    print(s.numberOfWays(10))
    print(s.numberOfWays(18))
