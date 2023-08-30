"""
so okay.. 

for last step to be at index-0
last-1 step needs be at index-0 and stay, or index-1 and left 
this opens up two possibilities
  0,stay
    last-2 step needs be at one of 
      0 stay
      1 left

  1,left
    last-2 step needs be at one of
      1 stay
      0 right
      2 left

"""


from functools import cache


class Solution:
    def numWays(self, steps: int, arrLen: int) -> int:
        
        # idx: position at step
        @cache
        def to(idx, step):
            if idx==0 and step==0:
              return 1
            
            if step == 0 and idx!=0:
               return 0
            
            lastStepMovedLeft = lastStepMovedRight = lastStepStayed = 0

            lastStepStayed = to(idx, step-1)
            if idx<arrLen-1:
              lastStepMovedLeft = to(idx+1, step-1)
            if idx>0:
              lastStepMovedRight = to(idx-1, step-1)
            
            return lastStepStayed + lastStepMovedLeft + lastStepMovedRight

        return to(0, steps)
    

if __name__ == '__main__':
   s = Solution()
   print(s.numWays( steps = 3, arrLen = 2))