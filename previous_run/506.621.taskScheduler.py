"""
https://leetcode.com/problems/task-scheduler/

It feels like it should prioritize the heaviest task which becomes eligible 
but that invovles the complextiy of pushing back ineligible ones..
"""


from collections import Counter, defaultdict
import heapq
from typing import List

from sortedcontainers import SortedList


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        C = Counter(tasks)

        h = []
        for task, count in C.items():
            heapq.heappush(h, (-count, 0))  # next time, remaining count

        time = 0
        while h:
            popped = []
            while h and h[0][1] > time:
                popped.append(heapq.heappop(h))

            if h:
                count, taskTime = heapq.heappop(h)
                if count+1:
                    heapq.heappush(h, (count+1, time+n+1))

            for p in popped:
                heapq.heappush(h, p)

            time += 1
        return time

"""
maybe I could use a queue per time
in each time queue, I use a heap to store the count
hmm.. very hard to program..

let me see, using a heap
sort by time, but field 1 being a sorted list, store the max count to the behind
"""


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        C = Counter(tasks)

        h = []
        sl = SortedList(C.values())
        heapq.heappush(h, (0, -sl[-1], sl)) # time, sl

        time = 0
        while h:
            
            if h[0][0] <= time:
                _, maxTask, sl = heapq.heappop(h)
                sl.pop()

                if sl:
                    heapq.heappush(h, (time+1, -sl[-1], sl))
                if maxTask + 1:
                    heapq.heappush(h, (time+1+n, maxTask + 1, SortedList([-maxTask-1])))
            
            while h and h[0][0] <= time:
                _, maxTask, sl = heapq.heappop(h)
                heapq.heappush(h, (time+1, maxTask, sl))

            time += 1
        return time

"""
note you don't need the sortedlist to push back 


"""


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        C = Counter(tasks)

        h = []
        sl = SortedList(C.values())
        heapq.heappush(h, (0, -sl[-1], sl))  # time, sl

        time = 0
        while h:

            if h[0][0] <= time:
                _, maxTask, sl = heapq.heappop(h)
                sl.pop()

                if sl:
                    heapq.heappush(h, (time+1, -sl[-1], sl))
                if maxTask + 1:
                    heapq.heappush(h, (time+1+n, maxTask + 1, [-maxTask-1]))

            while h and h[0][0] <= time:
                _, maxTask, sl = heapq.heappop(h)
                heapq.heappush(h, (time+1, maxTask, sl))

            time += 1
        return time

""""
a bit better 
Runtime: 786 ms, faster than 19.68% of Python3 online submissions for Task Scheduler.
Memory Usage: 14.9 MB, less than 12.70% of Python3 online submissions for Task Scheduler.

hmm.. when I first add them
why do I add them all as 0

I could sort them by count, then adding them sequentially right?
"""

        
class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        C = Counter(tasks)

        h = []
        for i,c in enumerate(sorted(C.values(), reverse=True)):
            heapq.heappush(h,(i,-c))
        
        time = 0
        while h:
            if h[0][0] <= time:
                _, negCount = heapq.heappop(h)
                if negCount+1:
                    heapq.heappush(h, (time+n+1, negCount+1))
            while h and h[0][0] <= time:
                _, count = heapq.heappop(h)
                heapq.heappush(h, (time+1, count))
            time += 1
        
        return time


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        C = Counter(tasks)

        h = []
        for i, c in enumerate(sorted(C.values(), reverse=True)):
            heapq.heappush(h, (i, -c))

        time = 0
        while h:
            while h[0][0] < time:
                _, count = heapq.heappop(h)
                heapq.heappush(h, (time, count))

            if h[0][0] <= time:
                _, negCount = heapq.heappop(h)
                if negCount+1:
                    heapq.heappush(h, (time+n+1, negCount+1))

            time += 1

        return time


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        C = Counter(tasks)

        h = []
        for i, c in enumerate(sorted(C.values(), reverse=True)):
            heapq.heappush(h, (i, -c))

        time = 0
        while h:
            popped = []
            while h and h[0][0] < time:
                popped.append(heapq.heappop(h)[1])
            
            for i,c in enumerate(sorted(popped)):
                heapq.heappush(h, (time+i, c))

            if h[0][0] <= time:
                _, negCount = heapq.heappop(h)
                if negCount+1:
                    heapq.heappush(h, (time+n+1, negCount+1))

            time += 1

        return time

"""
Runtime: 1131 ms, faster than 12.28% of Python3 online submissions for Task Scheduler.
Memory Usage: 14.2 MB, less than 99.67% of Python3 online submissions for Task Scheduler.
"""




class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        C = Counter(tasks)

        h = []
        for i, c in enumerate(sorted(C.values(), reverse=True)):
            heapq.heappush(h, (i, -c))

        time = 0
        skipped = []
        while h or skipped:
            skippedMaxTask = skipped[0][0] if skipped else float('inf')
            nextTaskCount = 0
            if h and h[0][0] <= time and -h[0][1] >= -skippedMaxTask:
                nextTaskCount = h[0][1]+1
                heapq.heappop(h)
            elif skipped:

                nextTaskCount = skippedMaxTask+1
                heapq.heappop(skipped)

            if nextTaskCount:
                heapq.heappush(h, (time+n+1, nextTaskCount))

            while h and h[0][0] <= time:
                taskTime, count = heapq.heappop(h)
                heapq.heappush(skipped, (count, taskTime))
            time += 1

        return time

"""
Runtime: 898 ms, faster than 16.13% of Python3 online submissions for Task Scheduler.
Memory Usage: 14.3 MB, less than 84.35% of Python3 online submissions for Task Scheduler.
"""


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        C = Counter(tasks)

        h = []
        for i, c in enumerate(sorted(C.values(), reverse=True)):
            heapq.heappush(h, (i, -c))

        time = 0
        skipped = SortedList()
        while h or skipped:
            skippedMaxTask = skipped[-1] if skipped else float('-inf')
            nextTaskCount = 0
            if h and h[0][0] <= time and -h[0][1] >= skippedMaxTask:
                nextTaskCount = h[0][1]+1
                heapq.heappop(h)
            elif skipped:
                nextTaskCount = -skippedMaxTask+1
                skipped.pop()

            if nextTaskCount:
                heapq.heappush(h, (time+n+1, nextTaskCount))

            while h and h[0][0] <= time:
                _, count = heapq.heappop(h)
                skipped.add(-count)
            time += 1

        return time

"""
Runtime: 1171 ms, faster than 11.60% of Python3 online submissions for Task Scheduler.
Memory Usage: 14.7 MB, less than 12.70% of Python3 online submissions for Task Scheduler.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.leastInterval(tasks=["A", "A", "A", "B", "B", "B"], n=2))
    print(s.leastInterval(tasks=["A", "A", "A", "B", "B", "B"], n=0))
    print(s.leastInterval(tasks=["A", "A", "A", "A",
          "A", "A", "B", "C", "D", "E", "F", "G"], n=2))

    print(s.leastInterval(["A", "A", "A", "B", "B", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]                          ,7))
