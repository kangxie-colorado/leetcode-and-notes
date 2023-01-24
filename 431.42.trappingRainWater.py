"""
https://leetcode.com/problems/trapping-rain-water/?envType=study-plan&id=algorithm-iii

I knew this can be solved by monotonic stack.. 
and also two pointers.. let me see
height = [0,1,0,2,1,0,1,3,2,1,2,1]

[0,1,0,2,1,0,1,3,2,1,2,1]
 l                     r

leftH=righH=0
check l,r, which is smaller
l<r: l->0
    ::incr + 0
    and move to 1

[0,1,0,2,1,0,1,3,2,1,2,1]
   l                 r
    lHeight = 0, rHeight =1 <- the lowest height will dominate the water 

wait.. actually the left/right ends are always 0
l,r can start with 1, n-2

l->1 r->2
    because l<r:
        calculate l-indx, min(lHeight-A[l], rHeight-A[r]) (+0)
        move l
        and because l>lHeight, lHeight=A[l]=1

l->0,r->2
    l<r:
        l-indx, lH-A[l] = 1, rH -A[l]=2->take 1 (+1)
        move l
        l < lHeight, lHeight doesn't change

l->2, r->2
    l<=r:
        l-indx, lH-A[l] = 0.. +0
        move l
        l > lHeight, lHeight = A[l] = 2

l->1,r->2
    l<r:
        lH=2 - A[l]=1 => 1
        rH=2 - A[l]=1 => 1 +1
        move l,
        A[l] < lHeight, no change
l->0,r->2
    l<r
        +? +2
        lH no change
l->1,r->2
    l<r
        +1
        lH no change

l->3,r->2
    l>r:
        rH-A[r]==-1 +0
        move r
        A[r]>rH.. rH=2

l->3,r->1
    l>r:
        rH-1 = 1 +1
        move r
        A[r]<rH.. no change
l->3,r->2
    l>r
        rH-2=0 + 0
        move r
        A[r]==rH, no change
l meets r.. end... 


        


"""


from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        lH,rH = height[0], height[-1]
        l,r = 1, len(height)-2
        water = 0
        while l<=r:
            if height[l] <= height[r]:
                water += max(0, min(lH,rH) - height[l])
                lH = max(lH, height[l])
                l+=1
            else:
                water += max(0, min(lH, rH) - height[r])
                rH = max(rH, height[r])
                r-=1
        return water

"""
okay.. as I felt.. it is not right
I think the pointer need to walk until it is smaller than one last position

i.e. after deal with first water, you need to walk two position (example 1)
and to start, the right needs to walk 2 positions as well... 

this way.. if lets say, the left is like 1,2,3,4,5,6 then 2 4 5 2 1
the left will walk across 6, right will walk acorss 5

yeah.. I felt it is not right when I was evolving on the top of the file
but didn't truly realize
"""


class Solution:
    def trap(self, height: List[int]) -> int:

        l=1
        while l<len(height)-1 and height[l]>=height[l-1]:
            l+=1
        
        r=len(height)-2
        while r>=0 and height[r]>=height[r+1]:
            r-=1

        lH, rH = height[l-1], height[r+1]
        water = 0
        while l <= r:
            if height[l] <= height[r]:
                water += min(lH, rH) - height[l]
                l += 1
                while l<=r and height[l] >= lH:
                    lH=height[l]
                    l+=1
            else:
                water += min(lH, rH) - height[r]
                r -= 1
                while height[r] >= rH:
                    rH = height[r]
                    r-=1
        return water

"""
okay.. I think maybe this is not what I remember it is.. 
okay.. let me go back to monotonic stack

finding first bigger value to left and right 
no.. maintain a decreasing stack

when an bigger value comes.. the stack top pops.. and it will become a local min
"""


class Solution:
    def trap(self, height: List[int]) -> int:
        stack = [height[0]]
        water = 0
        for num in height[1:]:
            while stack and stack[-1] < num:
                h = stack.pop()
                times = 1
                while stack and h == stack[-1]:
                    times+=1
                    stack.pop()

                if stack:
                    water += (min(stack[-1], num) - h)*times    
        return 0

"""
okay.. mind fart
did this before but cannot remember how to anymore... 

okay.. maybe next greater value???
and last greater value??

I think it should be greatest value to left, and to right 
okay.. I see

left scan, right scan and combine.. where is that two pointer solution
"""


class Solution:
    def trap(self, height: List[int]) -> int:   
        n = len(height)

        leftGreatest = [0]*n
        maxLeftH = 0
        for i,h in enumerate(height):
            leftGreatest[i] = max(maxLeftH, h)
            maxLeftH = leftGreatest[i]

        rightGreatest = [0]*n
        maxRightH = 0
        for i, h in enumerate(height[::-1]):
            rightGreatest[i] = max(maxRightH, h)
            maxRightH = rightGreatest[i]
        
        rightGreatest = rightGreatest[::-1]

        water = 0
        for i,h in enumerate(height):
            water += min(leftGreatest[i], rightGreatest[i]) - h
        return water

"""
Runtime: 139 ms, faster than 62.53% of Python3 online submissions for Trapping Rain Water.
Memory Usage: 16.1 MB, less than 17.38% of Python3 online submissions for Trapping Rain Water.

okay.. as I am doing this, I can kind of see the leftGreatest or rightGreatest only depends on last value
so it is like DP and only depends on last position

so that makes it two pointer like
so I see a glipmse of two pointers solution 

I was focus on wrong places.. let me re-think 
"""


class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)        
        l,r = 0,n-1
        lH, rH = height[l], height[r]
        
        water = 0
        while l<=r:
            # kind of like dp to calculate upto l/r, the max height to left,right
            lH = max(lH, height[l])
            rH = max(rH, height[r])
            minH = min(lH, rH)
            if height[l]<=height[r]:
                water += minH - height[l]
                l+=1
            else:
                water += minH - height[r]
                r-=1
                
        return water

"""
Runtime: 146 ms, faster than 57.18% of Python3 online submissions for Trapping Rain Water.
Memory Usage: 15.9 MB, less than 77.82% of Python3 online submissions for Trapping Rain Water.


compare the dp solution to two pointers solution
dp soulution, at each point we know globally the min l/r height to use by taking

        for i,h in enumerate(height):
            water += min(leftGreatest[i], rightGreatest[i]) - h

but in two pointer solution we need this test to route to different branches
            if height[l]<=height[r]:
                water += minH - height[l]
                l+=1
            else:
                water += minH - height[r]
                r-=1
        
        why?
        because here we only know for sure
            height[l] <= lH
            height[r] <= lR

        we don't have the absolte relationship between height[l] vs lR and the other pair
        so we take the smaller of height[l],height[r] to make sure it is absolutely the min in these two pairs..

        why not taking the bigger to calculate? that will render the whole algorithm unstable ...



"""


if __name__ == '__main__':
    s = Solution()
    print(s.trap(height=[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))
    print(s.trap(height=[4, 2, 0, 3, 2, 5]))
