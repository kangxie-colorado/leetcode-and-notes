"""
https://leetcode.com/problems/meeting-scheduler/?envType=study-plan&id=algorithm-iii


line sweep?

Input: slots1 = [[10,50],[60,120],[140,210]], slots2 = [[0,15],[60,70]], duration = 8

scan thru both 
slots1 ->
10  50  60  120 140 210
1   0   1    0   1   0
slots2 ->
0 10  15 50  60  70 120 140 210
1  2  1  0   2    1  0   1   0

looks like I can combine slots1/slots2 and sort to scan to reach the same 

then I search 
when I see a 2.. I look forward if it is enough duration... I return this [point,point+duration]
if the duration is not enough, continue to scan 

could give a try
"""


from typing import List


class Solution:
    def minAvailableDuration(self, slots1: List[List[int]], slots2: List[List[int]], duration: int) -> List[int]:
        events = []
        
        # actually I should merge then sort 
        # just sort the events - if start/end land on the same point (what to do?)
        for s,e in slots1+slots2:
            events.append((s,1))
            events.append((e,-1))

        events.sort()
        avail = 0
        for i, (t,incr) in enumerate(events):
            avail+=incr

            if avail>=2:
                if i+1<len(events) and events[i+1][0]-t >= duration:
                    return [t, t+duration]
        return []


"""
Runtime: 646 ms, faster than 49.30% of Python3 online submissions for Meeting Scheduler.
Memory Usage: 23.7 MB, less than 5.10% of Python3 online submissions for Meeting Scheduler.

two pointers?
sort slots1/slots2 and i=j=0

if they overlap by duration.. return something 
else. move the smaller end interval????

slots1 = [[10,50],[60,120],[140,210]],      i starts with 0
slots2 = [[0,15],[60,70]],                  j starts with 0
duration = 8     

(10,50) vs (0,15) not enough move j (or i?)
hmm.. looks like I should move j (the one with smaller end indeed)

give a try

"""


class Solution:
    def minAvailableDuration(self, slots1: List[List[int]], slots2: List[List[int]], duration: int) -> List[int]:
        slots1.sort(key=lambda x: x[1])
        slots2.sort(key=lambda x: x[1])

        i=j=0
        while i<len(slots1) and j<len(slots2):
            s1,e1 = slots1[i]
            s2,e2 = slots2[j]

            if min(e1,e2) >= max(s1,s2)+duration:
                return [max(s1,s2), max(s1, s2)+duration]
            
            if e1 < e2:
                i+=1
            else:
                j+=1
        
        return []
"""
Runtime: 574 ms, faster than 81.93% of Python3 online submissions for Meeting Scheduler.
Memory Usage: 21.5 MB, less than 85.36% of Python3 online submissions for Meeting Scheduler.
ah.. sort itself, not combined.. why do I need a lambda x:x[1]
"""


class Solution:
    def minAvailableDuration(self, slots1: List[List[int]], slots2: List[List[int]], duration: int) -> List[int]:
        slots1.sort()
        slots2.sort()

        i = j = 0
        while i < len(slots1) and j < len(slots2):
            s1, e1 = slots1[i]
            s2, e2 = slots2[j]

            if min(e1, e2) >= max(s1, s2)+duration:
                return [max(s1, s2), max(s1, s2)+duration]

            if e1 < e2:
                i += 1
            else:
                j += 1

        return []



if __name__ == '__main__':
    s = Solution()
    print(s.minAvailableDuration(slots1=[[10, 50], [60, 120], [
          140, 210]], slots2=[[0, 15], [60, 70]], duration=8))
    print(s.minAvailableDuration(slots1=[[10, 50], [60, 120], [
          140, 210]], slots2=[[0, 15], [60, 70]], duration=12))
