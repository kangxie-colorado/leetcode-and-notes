"""
https://leetcode.com/problems/minimum-cost-tree-from-leaf-values/

because each node has to have 0 or two children
so this is a balanced tree?

not necessarily true 

okay.. 
so base is 2 nodes.. there is only one way to form

3? 
    - using the 2 nodes tree as left, 
    - 3 join 2: downgrade 2 to form a subtree with 3
    so I get two forms
4? 
    - using the 3 nodes tree as left tree - 2 forms
        meaning add a new root and 4 to be to right 

    - 4 join 3
    so I get four forms
so on and so forth

let me see the impliction for forming each way
1. adding a new root.. it basically means the root will be 
    max children * right 
    (maxLeft, maxRight) can be stored in each node
    actually the maxLeft will be the max prior to last element

2. downgrade last node and form a new subtree
    this subtree's maxChild will be right 
    previous parent's maxLeft will be the same 
    but it will propogate differently 
    but observe that
        previously last node is the max... say thats R1
        R1 will be in the final prod anyway.. removing it from prod, prod//R1
        then we add a new R2(the new right), the new prod will be prod//R1*R2
        wait... the previous might be in the prod?
        nope.. it will definitely be in the prod...

        nah.. it could be R1 or the one before R1
        hmm... 
        not yet figured out let me cont 

lets say we keep maxLeft, maxRight after adding each element 

using n-1 nodes as left, 
    maxLeft = max(maxLeft, maxRight) at n-1
    maxRight = A[n]

using n-1 th node to form a subtree
    note this node has to be the right most subtree
    maxLeft = maxLeft at n-1
    maxRight = max(maxRight at n-1, A[n])
yeah.. looks like I have the equation now 
run some examples

 arr = [6,2,4]
   i           1  2
maxL,maxR    6,2  6,4  
maxR,maxR    6,2  6,4

on 4, using prev as left tree 6,4
form with 2... 6,4

but damn.. it wants all the sum of non-leaf node.. 
I probably can still do the same or similar transition

using as left, maxL, maxR is like above
sum changes from oldSum to oldSum + (maxL*maxR)

   i              1          2
maxL,maxR,sum    6,2,12    6,4,36
maxR,maxR,sum    6,2,12    6,4,?

form a new subtree, maxL,maxR is like above
sum changes from oldSum to 
    - first a new node appears, which A[n]*A[n-1]
    - an old node will disappear which A[n-1]*A[n-2]
    the delta is the sum change????????? delta can be but the disappearing sum is the sum at n-1?
    nah.. that is the total... 
    hmm.... n-1 node can be at right most or forming a subtree with n-1 node
        so the disappearing sum is 
            either the root (maxL*maxR at n-1)
            or A[n-1]*A[n-2]
            see which delta is smaller??
            maybe.. 

so adding 4
    - if 2 is the right most, root disappears, which is 2*6 -12 (+8) (36-4 = 32)
    - is 6,2 is some deeper level, their parent disappears which is 12.. also +8.. same

but let me adding a 5
6,2,4,5

   i              1          2        3
maxL,maxR,sum    6,2,12    6,4,36     6,5,                                  # using as a left
maxR,maxR,sum    6,2,12    6,4,32                               # form a new subtree


on 5:
using prev as a left 
two paths..
    6,5,66
    6,5,62 <= choose this

break last node which is 4
two paths
    4 is the child of root...
        -24 + 20, 6,5,? -- wait... the new nodes is 20, the root is 24
        the root will be become 30 (6*5)
        the new internal node will be 20 
        so the delta is 30-24+20 = 26
        6,5,36+26=62
    4 is the deeper right most
        the root will change from (6*4=24) to 30
        the disappearing will be -8 (will be replaced by 10 or smaller depending on A[n] vs A[n-1])
        the new node will be 20
        so the delta is 30-8+20-24+10 = 28
        6,5,32+28=60
    so the new min is 62
    and I am wrong.. it should be 58

okay.. turns out [2,4] as previous right subtree's leaf can be used at right then left subtree -- with 5 
so using previous as left tree has more forms... 

in other ways, 5 can be right to [2,4] or [6,2,4] -- or maybe to [4] - this generalizes things
let me think this way

let me eat and maybe exercise first 

while I was walking I see the thoughts drain is heading to wrong direction 
even you figure out adding one element vs the existent sequence, then what?

adding next element, how many forms of this tree do you keep?
that's not gonna to work in reality

so I think this should be a area dp, not a sequential dp
i.e. draw some line, i, i>=1 
A[:i] will be left tree
A[i:] will be in the right tree

base is when A is only 1 element, it must be a leaf
what is passed from children to parent nodes?

a maxChild and a total non-leaf sum, right?

lets give a try

"""


from typing import List


class Solution:
    def mctFromLeafValues(self, arr: List[int]) -> int:
        
        def f(A):
            if len(A) == 1:
                return A[0], 0 # max child and internal node sum
            
            total = float('inf')
            maxChild = 0
            for i in range(1,len(A)):
                leftMax, leftSum = f(A[:i])
                rightMax, rightSum = f(A[i:])
                treeTotal = leftSum+rightSum+leftMax*rightMax

                if treeTotal < total:
                    total = treeTotal
                    maxChild = max(maxChild, leftMax, rightMax)
            return maxChild, total
        return f(arr)[1]

"""
as expected  TLE at
[8,14,7,7,13,14,1,3,5,9,5,1,8,15,7,6]

adding cache.. but list is unhashable..
so change A to i-j
"""


class Solution:
    def mctFromLeafValues(self, A: List[int]) -> int:

        def f(i,j):
            # [i,j) right open? or not
            if i==j-1:
                return A[i], 0  # max child and internal node sum

            total = float('inf')
            maxChild = 0
            for k in range(i+1, j):
                leftMax, leftSum = f(i,k)
                rightMax, rightSum = f(k, j)
                treeTotal = leftSum+rightSum+leftMax*rightMax

                if treeTotal < total:
                    total = treeTotal
                    maxChild = max(maxChild, leftMax, rightMax)
            return maxChild, total
        return f(0,len(A))[1]

"""
Runtime: 117 ms, faster than 38.70% of Python3 online submissions for Minimum Cost Tree From Leaf Values.
Memory Usage: 15 MB, less than 6.23% of Python3 online submissions for Minimum Cost Tree From Leaf Values.

let me see bottom up?

yea, like the palindrom DP
this can use half of the matrix 

e.g. 6 2 4 5
    6     2        4       5
6  6,0   6,12    6,32
2        2,0     4,8     5,28
4                4,0     5,20
5                        5,0

dp[i][j] represents the (maxChild, totalSum) for A[i:j+1] meaning i,j are both inclusive 
when i==j, base A[i],0
when i==j-1, actuall also base max(A[i],A[j]),A[i]*A[j] or it can be deducted from last base 

then 
dp[i][j] = choice {
    from dp[i][j-1] vs A[j], max1,sum1: max(max1, A[j]), sum1+max1*A[j]
    from dp[i+1][j] vs A[i], max2,sum2: max(A[i], max2), sum2+max2*A[i]
}

using this to solve above
dp[0][2] : 6 2 4
    from left: dp[i][j-1]={6,12} vs 4.. max=>6, sum=>12+24=36
    from below: dp[i+1][j]={?} vs 6 so this need to fill from the bottom.. like palindrom
    okay below is 4,8... {4,8} vs 6.. max=>6, sum=>8+4*6=32 (choice)

dp[1][3] : 2 4 5
    from left {4,8} vs 5 => max:5, sum:8+4*5=28 (choice)
    from below {5,20} vs 2 => max:5, sum:20 + 5*2 = 30

dp[0][3] : 6 2  4 5
    from left {6,32} vs 5: max:6, sum: 32+5*6=62
    from below {5,28} vs 6: max: 6, sum: 28+5*6 = 58 (choice and right answer)
    woww!!
"""

def print_this(A, dp):
    s1 = s2 = "            "
    
    for i,val in enumerate(A):
        s1 = f"{s1} {i:<10}"
        s2 = f"{s2} {val:<10}"
    print(s1)
    print(s2)
    for i,row in enumerate(dp):
        s = f"idx={i},{A[i]:<5}"
        for p in row:
            tup = f"{p}"
            s = f"{s} {tup:<10}"
        print(s)

class Solution:
    def mctFromLeafValues(self, A: List[int]) -> int:
        n = len(A)
        dp = [ [(0,0)] *n for _ in range(n)]

        for i in range(n-1,-1,-1):
            for j in range(i,n):
                if i==j:
                    dp[i][j] = (A[i],0)
                elif i==j-1:
                    dp[i][j] = (max(A[i],A[j]), A[i]*A[j])
                else:
                    # from left 
                    leftMax, leftSum = dp[i][j-1]
                    belowMax, belowSum = dp[i+1][j]

                    if leftSum+leftMax*A[j] < belowSum+belowMax*A[i]:
                        dp[i][j] = (max(leftMax, A[j]), leftSum+leftMax*A[j])
                    else:
                        dp[i][j] = (max(belowMax, A[i]), belowSum+belowMax*A[i])
        


        print_this(A,dp)
        return dp[0][n-1][1]
                    
"""
s-macbook-pro:leetcode-and-notes xiekang$ python3 412.1130.minCostFromLeafVals.py 
             0          1          2          3          4          5          6          7         
             3          7          2          12         15         10         3          9         
idx=0,3     (3, 0)     (7, 21)    (7, 35)    (12, 119)  (15, 299)  (15, 449)  (15, 494)  (15, 627) 
idx=1,7     (0, 0)     (7, 0)     (7, 14)    (12, 98)   (15, 278)  (15, 428)  (15, 473)  (15, 582) 
idx=2,2     (0, 0)     (0, 0)     (2, 0)     (12, 24)   (15, 204)  (15, 354)  (15, 390)  (15, 477) 
idx=3,12    (0, 0)     (0, 0)     (0, 0)     (12, 0)    (15, 180)  (15, 330)  (15, 360)  (15, 447) 
idx=4,15    (0, 0)     (0, 0)     (0, 0)     (0, 0)     (15, 0)    (15, 150)  (15, 180)  (15, 267) 
idx=5,10    (0, 0)     (0, 0)     (0, 0)     (0, 0)     (0, 0)     (10, 0)    (10, 30)   (10, 117) 
idx=6,3     (0, 0)     (0, 0)     (0, 0)     (0, 0)     (0, 0)     (0, 0)     (3, 0)     (9, 27)   
idx=7,9     (0, 0)     (0, 0)     (0, 0)     (0, 0)     (0, 0)     (0, 0)     (0, 0)     (9, 0)    

cool.. I got something like this
then I use the leetcode to help me figure out where it was wrong

I narrowed down to 2,12,15,10 which is 354, dp[2][5]
also 12 15 10 3 which is 260 dp[3][6]
they are right

but dp[2][6] i.e. 2,12,15,10,3 is wrong.. 
okay let me see

yeah.. I only consider left once.. but it can go to up to the diagnoal line
[2,12,15,10,3] i.e. dp[2][6]
can also be from dp[2][4] ([2,12,15]) vs dp[5][6]([10,3]).. i.e 15,204 vs 10,30

which will form 
    max = max(15,10) = 15
    sum = 205+30+15*10=384 and happend to be the right answer here.. 

so.. that single element can be generalized to 
dp[2][6] can be formed by {
    dp[2][5] vs dp[6][6] 
    dp[2][4] vs dp[5][6]
    dp[2][3] vs dp[4][6]
    dp[2][2] vs dp[3][6]

    # notice the changing happens in the inside.. 
    # very interesting...
}

"""


class Solution:
    def mctFromLeafValues(self, A: List[int]) -> int:
        n = len(A)
        dp = [[(0, 0)] * n for _ in range(n)]

        for i in range(n-1, -1, -1):
            for j in range(i, n):
                if i == j:
                    dp[i][j] = (A[i], 0)
                elif i == j-1:
                    dp[i][j] = (max(A[i], A[j]), A[i]*A[j])
                else:
                    sumIJ = float('inf')
                    maxIJ = 0
                    for k in range(1,j-i+1):
                        leftMax, leftSum = dp[i][j-k]
                        belowMax, belowSum = dp[j-k+1][j]

                        newMax = max(leftMax, belowMax)
                        newSum = leftSum + leftMax*belowMax + belowSum
                        if newSum < sumIJ:
                            sumIJ = newSum
                            maxIJ = newMax
                    dp[i][j] = (maxIJ, sumIJ)

        # print_this(A, dp)
        return dp[0][n-1][1]

"""
Runtime: 122 ms, faster than 38.54% of Python3 online submissions for Minimum Cost Tree From Leaf Values.
Memory Usage: 14.1 MB, less than 30.21% of Python3 online submissions for Minimum Cost Tree From Leaf Values.

me goodnes.. 
I need to read this
https://leetcode.com/problems/minimum-cost-tree-from-leaf-values/discuss/339959/One-Pass-O(N)-Time-and-Space
also
https://leetcode.com/problems/minimum-cost-tree-from-leaf-values/discuss/478708/RZ-Summary-of-all-the-solutions-I-have-learned-from-Discuss-in-Python

but lets take a snap 

okay.. here is what I learned 
1. DP is brute force searching with memoerization -- not surprised 
    DP does many unnecessary calculation 
    why unnecessary, becausre there are short cut
    the insights is hard to come up for me really! but here it is
2. because fo the rules, the bigger node is contributing for more levels than smaller node
    so we want to keep the bigger node as close as possible to root
    that means we want to keep min node as close as to the deepest level
3. therefore, we work around the min
    and see which neightbor this min wants to form an internal node with 
    and so on and so forthe
lets give a try
"""


class Solution:
    def mctFromLeafValues(self, A: List[int]) -> int:

        res = 0
        while len(A)>2:
            minIdx = A.index(min(A))
            if 0<minIdx<len(A)-1:
                res += A[minIdx]*min(A[minIdx+1], A[minIdx-1])
            else:
                if minIdx:
                    # n-1
                    res += A[minIdx]*A[minIdx-1]
                else:
                    # 0
                    res += A[minIdx]*A[minIdx+1]
            A.pop(minIdx)
        return res + A[0]*A[1]

"""
Runtime: 38 ms, faster than 80.21% of Python3 online submissions for Minimum Cost Tree From Leaf Values.
Memory Usage: 13.8 MB, less than 74.74% of Python3 online submissions for Minimum Cost Tree From Leaf Values.

okay.. one last touch...
we are searching for min(A) repeatedly and there can be optimization to that

we keep a monotonic stack, that is decreasing 
so when an upcoming element is bigger than the stack top
pop it.. and interesting things happen here

the stack top is bigger than it.. the upcoming is bigger than it..
thus it is a local min.. 

e.g 
    6 2 4 5

stack -> grows to right
|| stack: inf 6 2
on 4, top is < 4, pop->2
2<4 and 2<6... it is a local min.. 2 can form with 4; contri-8
|| stack: inf 6 4

same, on 5, 4 becomes a local min.. 4 to form with 5; contri-20
|| stack: inf 6 5

now, just take the top two of stack, contri-30
8+20+50 = 58

e.g.
    6 2 4 5 1

upto 5, 8+20 and stack is 
|| stack: inf 6 5

on 1.. it just append
|| stack: inf 6 5 1

now 1 can only form with 5, +5
and 5 can only form with 6, +30
28+5+30 = 63

and it is correct
lets code it up

one thing I didn't think is eqaul case... 
but e.g. 4 2 2, the 2 should be formed with 2 so later equal should trigger pop as it seems to be
"""


class Solution:
    def mctFromLeafValues(self, A: List[int]) -> int:
        # a guardian value so no need to test stack to be empty 
        # also it provides an non-effective number to min comparison 
        stack = [float('inf')]
        res = 0
        for num in A:
            while stack[-1] <= num:
                top = stack.pop()
                res += top * min(stack[-1], num)
            stack.append(num)
        while len(stack)>2:
            res += stack.pop() * stack[-1]
        return res

"""
Runtime: 32 ms, faster than 93.49% of Python3 online submissions for Minimum Cost Tree From Leaf Values.
Memory Usage: 13.8 MB, less than 74.74% of Python3 online submissions for Minimum Cost Tree From Leaf Values.
"""

if __name__ == '__main__':
    s = Solution()
    # print(s.mctFromLeafValues(A=[6, 2, 4]))
    # print(s.mctFromLeafValues(A=[6, 2, 4, 5]))
    print(s.mctFromLeafValues(A=[3, 7, 2, 12, 15, 10, 3, 9]))
