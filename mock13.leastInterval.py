"""
naturally heap
and the sorting is based on most task remained and next running time

(time, -remain)
"""

from collections import Counter
import heapq
from typing import List


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        C = Counter(tasks)
        h = []
        for t,count in enumerate(sorted(C.values(), reverse=True)):
            heapq.heappush(h, (t,-count))
        
        res = 0
        while h:
            t,count = heapq.heappop(h)
            res = max(res, t)
            if abs(count)>0:
                heapq.heappush(h, (t+n, -(abs(count)-1)))
        
        return res
"""
there is a stupid car, parking and running 
making me distracted and above is logicall error
so I need to simulate the time?

wait a sec, think some more before coding again
if I just introduce the time to control
"""

class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        C = Counter(tasks)
        h = []
        for t,count in enumerate(sorted(C.values(), reverse=True)):
            heapq.heappush(h, (t,-count))
        
        
        time = 0
        while h:
            if h[0][0] <= time:
              t,count = heapq.heappop(h)
              if abs(count)>1:
                  heapq.heappush(h, (time+n+1, count+1))
            time += 1
        
        return time

"""
okay.. the error is the priority is not fully correct
if I prioritize the remain, the time maybe

it may involve pop and push back???
"""
class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        C = Counter(tasks)
        h = []
        for t,count in enumerate(sorted(C.values(), reverse=True)):
            heapq.heappush(h, (t,-count))
        
        
        time = 0
        while h:
            if h[0][0] <= time:
              t,count = heapq.heappop(h)
              while h and h[0][0]<=time and h[0][1] < count:
                  heapq.heappush(h, (time+1, count))
                  t,count = heapq.heappop(h)

              if abs(count)>1:
                  heapq.heappush(h, (time+n+1, count+1))
            time += 1
        
        return time


if __name__ == '__main__':
    s = Solution()
    print(s.leastInterval(tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"], n = 2))