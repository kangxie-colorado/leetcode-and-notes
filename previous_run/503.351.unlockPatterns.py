"""
https://leetcode.com/problems/android-unlock-patterns/

at least m, at most n
so it translate to: sum(f(k) for k in range(m,n+1))?

if there any evolution between f(i) vs f(i-1)

I guess, if has to do with the i,j positions 

if i,j are such pair (not exclusive)
1,2 | 2,3 | 1,4 | 1,5... 
i.e they don't cross any number.. 

wait.. k is the total number not the digits.. I set a trap myself
so just backtracking?

f(i, run)
    i>k:
        all keys placed
        return 1
    for j in range(1,10):
        if j is eligible()
            res += f(j, run+[j])
    return res

yeah.. this seems it might work let me see

"""


class Solution:
    def numberOfPatterns(self, m: int, n: int) -> int:

        def eligible(curr,run):
            last = run[-1]
            x1,y1 = (last-1)//3, (last-1)%3
            x2, y2 = (curr-1)//3, (curr-1) % 3

            res = True
            if (x1 == x2 and abs(y1-y2) == 2) or (abs(x1-x2) == 2 and y1 == y2) or (abs(y1-y2) == 2 and abs(x1-x2) == 2):
                # same row or column or diagonal: check if mid point is in the set
                res = (3*(x1+x2)//2 + (y1+y2)//2 + 1) in run
            
            return res
            

        def f(k, run):
            if k==0:
                return 1
            
            res = 0
            for i in range(1,10):
                if run and (i in run or not eligible(i, run)):
                    continue

                res += f(k-1,run+[i])
            
            return res

                
        return sum(f(k,[]) for k in range(m,n+1))

"""
Runtime: 1582 ms, faster than 21.42% of Python3 online submissions for Android Unlock Patterns.
Memory Usage: 13.9 MB, less than 53.30% of Python3 online submissions for Android Unlock Patterns.

of course, I can use bitmap to make it cachable let me try
"""


class Solution:
    def numberOfPatterns(self, m: int, n: int) -> int:

        def eligible(curr, run, last):
            x1, y1 = (last-1)//3, (last-1) % 3
            x2, y2 = (curr-1)//3, (curr-1) % 3

            res = True
            if (x1 == x2 and abs(y1-y2) == 2) or (abs(x1-x2) == 2 and y1 == y2) or (abs(y1-y2) == 2 and abs(x1-x2) == 2):
                # same row or column or diagonal: check if mid point is in the set
                res = 1<<(3*(x1+x2)//2 + (y1+y2)//2 + 1) & run

            return res

        def f(k, run, lastBit):
            if k == 0:
                return 1

            res = 0
            for i in range(1, 10):
                if run and ((1<<i & run) or not eligible(i, run, lastBit)):
                    continue

                res += f(k-1, run|(1<<i), i)

            return res

        return sum(f(k, 0, 0) for k in range(m, n+1))

"""
Runtime: 1617 ms, faster than 21.42% of Python3 online submissions for Android Unlock Patterns.
Memory Usage: 13.8 MB, less than 91.21% of Python3 online submissions for Android Unlock Patterns.

Runtime: 176 ms, faster than 97.80% of Python3 online submissions for Android Unlock Patterns.
Memory Usage: 22 MB, less than 8.24% of Python3 online submissions for Android Unlock Patterns.

adding cache to both function.. 
"""
    
if __name__ == '__main__':
    s = Solution()
    print(s.numberOfPatterns(m=1, n=1))
    print(s.numberOfPatterns(m=1, n=2))
