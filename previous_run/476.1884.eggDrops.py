"""
https://leetcode.com/problems/egg-drop-with-2-eggs-and-n-floors/?envType=study-plan&id=dynamic-programming-iii

WTF?
so how to think this problem?

first if there is only one egg left.. you can only start from last known min_unbroken+1 floor and try one by one..
so the max is f (or f+1?)

n=0: 0<=f<=n and at floor f, it doesn't break... so no need to do anything -> 0
n=1: drop one egg at floor 1, it either breaks(f->0) or not(f->1) -> 1
n=2: drop one egg at f1 and another at f2.. 
    depending on how many eggs break.. f could be in 0,1,2
    steps 2
n=3: 2
n=4: 3
n=5: 3
n=6: 3
n=7: 4

kaoy... I tried to sort out the states
the decision tree

I buried myself with binary serach like decision tree
but ended up nowhere... 

I am beaten.. the first problem in DP III plan.. gosh.. not a good sign..
anyway.. time to learn

okay.. learned it 

"""
from functools import cache

class Solution:
    def twoEggDrop(self, n: int) -> int:
        
        @cache 
        def d(f):
            if f <= 1:
                return f
            return min(
                1+max(
                    i-1,
                    d(f-i)
                ) for i in range(1,f)
            )
        
        return d(n)

"""
Runtime: 2801 ms, faster than 40.92% of Python3 online submissions for Egg Drop With 2 Eggs and N Floors.
Memory Usage: 16.8 MB, less than 10.84% of Python3 online submissions for Egg Drop With 2 Eggs and N Floors.

change to bottom up dp? 
not a simple form change.. bottom up is totally different approach
it try to see how high we can reach (decide which floor is the f) with 2(k) eggs and m moves

    dp[m] = 1 + dp[m - 1] + m - 1;
I guess
    - dp[i] represents in i moves, how high I can reach 

    1 + dp[m - 1]: last egg does't break at m-1 move, i can test one more floor
        note.. you can only test only one more floor for a certainty 
        2 more floors.. if it breaks.. say at K+2 floor it break you don't know if K+1 it will break or not.. you skip it
        so only one more floor
    m - 1: if last egg breaks.. why m-1?
        if it breaks.. it has to be...

I think I might be totally confused about the understanding
    dp[m-1] is how many level can be veified with m-1 moves 
    m-1 is last egg breaks.. but it might be meaning prior to that, the egg didn't break 
    hmm... why adding them together 

====== back again to think this 
    dp[m] = 1 + dp[m - 1] + m - 1;
          = m + dp[m-1]
          = m + (m-1 + dp[m-2])
          = m + (m-1) + (m-2 + dp[m-3])
          ... this is actually a recursive definition 

    hard to explain but beautiful



"""

class Solution:
    def twoEggDrop(self, n: int) -> int:
        dp = [[0]*3]*(n+1)
        for m in range(1,n+1):
            for k in range(1,3):
                dp[m][k] = dp[m-1][k-1] + dp[m-1][k]+1
            if dp[m][k] >= n:
                return m
    

if __name__ == '__main__':
    s = Solution()
    print(s.twoEggDrop(2))
    print(s.twoEggDrop(100))