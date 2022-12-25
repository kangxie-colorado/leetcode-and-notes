"""
https://leetcode.com/problems/the-skyline-problem/


I thought using heap
but seems like I don't need to at this point

this is how I thought
just going thru the list, since it is already sorted 

keep the overlapping idx..
once the overlapping stopped, process this batch

now sort it by height (reverse), tie breaker being the left 
going thru them one by one again

keeping a merged list of ranges, it could be more than one range but at the end its going to become one range

res will be kept separately
for each new interval, compare with the merged ranges... update the results.. then merge the range
pay no attention to right side.. it is already determined 

probably not going to pass but give a try

"""


from heapq import heappush, heappop
import heapq
from typing import List

from sortedcontainers import SortedList


class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        def overlap(r1, r2):
            return not (r1[1]<r2[0] or r1[0]>r2[1])
        

        res = []
        def processOverlapBlds(blds):
            mergedBlds = [blds[0]]
            resTemp = [[blds[0][0], blds[0][2]]]
            for bld in blds[1:]:
                tmp = list(bld)
                newMergedBlds = []
                # merge fist, then see the merged temp vs the merged?
                # nah... 
                for i, mergedBld in enumerate(mergedBlds):
                    mergedBld = mergedBlds[i]
                    if overlap(bld, mergedBld):
                        if bld[0] < mergedBld[0]:
                            resTemp.append([bld[0], bld[2]])
                        if bld[1] > mergedBld[1]:
                            resTemp.append([mergedBld[1], bld[2]])
                        
                        tmp = [min(tmp[0], mergedBld[0]), max(
                            tmp[1], mergedBld[1]), mergedBld[2]]
                    elif tmp[1] < mergedBld[0]:
                        resTemp.append([bld[0], bld[2]])
                        break
                    else:
                        resTemp.append([bld[0], bld[2]])
                        newMergedBlds.append(mergedBld)

                newMergedBlds.append(tmp)
                newMergedBlds.extend(mergedBlds[i+1:])
                mergedBlds = newMergedBlds
            resTemp.sort()
            i = 0
            while i < len(resTemp) :
                res.append(resTemp[i])
                j = i+1
                while j<len(resTemp) and resTemp[j][1] == resTemp[i][1]:
                    j+=1
                i=j
            res.append([mergedBlds[-1][1], 0])
            
        overlapStart = 0
        overlapIdx = 1
        testRange = buildings[0]
        while overlapIdx < len(buildings):
            if not overlap(buildings[overlapIdx], testRange):
                # buildings[overlapStart:overlapIdx] are overlapping
                # process it
                overlapBuildings = buildings[overlapStart:overlapIdx]
                overlapBuildings.sort(key=lambda x: x[2], reverse=True)
                processOverlapBlds(overlapBuildings)

                # continue to next overlapping 
                overlapStart = overlapIdx

            testRange = [min(testRange[0], buildings[overlapIdx][0]), max(
                testRange[1], buildings[overlapIdx][1]), 0]
            overlapIdx += 1
        
        overlapBuildings = buildings[overlapStart:overlapIdx]
        overlapBuildings.sort(key=lambda x: x[2], reverse=True)
        processOverlapBlds(overlapBuildings)
        
        return res

"""
okay... spent that much time but ended up with no solution
I shall limit my thinking time to any problem to 45 mins.. there is no point going over that limit 

especially when I begin to tackle hard problems, and can easily get lost 
so I learned two solutions for this problem now

both use that line-sweep method
treat the start of building and end of building as isolated events

let me code it up
"""


class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        events = []

        for l,r,h  in buildings:
            # for entering events, we can use a separate filed to represent its type (-1 or 1)
            # but considering the tie breaker on equal x (the coordinates) is processing max height first
            # therefore I just use negative height so when I sort the max height will stay in the front
            # also for tie breaker on equal x but different events: entering vs leaving
            # we should always process the entering events first.. otherwise you end dropping to 0
            # prematurely, so entering event with negative height will also naturally come before 
            # leaving events which would be positive heights... and that happen to take care of processing
            # min height first.. otherwise, if you process max height when leaving.. it will pollute the results
            # for the ideas behind this.. check Hua Hua video explanation 
            events.append((l, -h)) 
            events.append((r, h))
        events.sort()
        
        res = []
        # the sorted list is the bookkeeping of the current active building heights
        # on entering event.. it will add the, on the leaving event, it will remove the event
        # removing is by key.. so that makes heap harder but balanced bst will do
        # sortedlist is like bst
        # init with a 0  so the 2nd max height is always in the sl
        # no need to special handle the dropping to 0 leaving events
        sl = SortedList([0]) 
        for x,h in events:
            if h<0:
                if abs(h) > abs(sl[-1]):
                    res.append([x,abs(h)])
                sl.add(abs(h))
            else:
                sl.remove(h)
                # if the tallest building leaves.. i.e. the max height changes
                if h>sl[-1]:
                    res.append([x,abs(sl[-1])])
        
        return res

"""
Runtime: 142 ms, faster than 83.66% of Python3 online submissions for The Skyline Problem.
Memory Usage: 20.3 MB, less than 36.35% of Python3 online submissions for The Skyline Problem.
"""

"""
okay
I see another solution using a heap

but only honer the entering eventing with its negative heights
treat the leaving eventing with zero heights and do housekeeping at that point

it kind of feels like sliding window...
"""


class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        events = []

        for l, r, h in buildings:
            # same idea.. also use negative to maintain the order
            events.append((l, -h))
            events.append((r, 0))
        events.sort()

        res = []
        heap = []
        for x,height in events:

            while height==0 and heap and heap[-1][0] < x:
                # leaving。。
                ...
                # okay.. I didn't fully understand the solution yet
                # be humble yourself.. copy and debug to understand 
                # ah.. I see.. it dishoner the right side of building
                # but it records the R as the buildings ending position 
                # so that only when the building has been totally passed it shall be popped 
                # code it up again (after seeing below other people's solution )


class Solution(object):
    def getSkyline(self, buildings):
        # add start-building events
        # also add end-building events(acts as buildings with 0 height)
        # and sort the events in left -> right order
        events = [(L, -H, R) for L, R, H in buildings]
        events += list({(R, 0, 0) for _, R, _ in buildings})
        events.sort()

        # res: result, [x, height]
        # live: heap, [-height, ending position]
        res = [[0, 0]]
        live = [(0, float("inf"))]
        for pos, negH, R in events:
            # 1, pop buildings that are already ended
            # 2, if it's the start-building event, make the building alive
            # 3, if previous keypoint height != current highest height, edit the result
            print(f"event: {pos} {negH} {R}")
            print(f"res: {res}, heap: {live}")
            while live[0][1] <= pos:
                heappop(live)
            print(f"heap: {live}")
            if negH:
                heappush(live, (negH, R))
            print(f"heap: {live}")
            if res[-1][1] != -live[0][0]:
                res += [[pos, -live[0][0]]]
            
            print()
        return res[1:]


class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        events = []

        for l, r, h in buildings:
            # same idea.. also use negative to maintain the order
            events.append((l, -h, r))
            
            events.append((r, 0, 0))
        events.sort()

        # this is to test if last max height is same as current height
        # when the max height changes, the outline should append a value
        res = [[0,0]] 
        # maxHeap is of course the (-height, ending position)
        # so basically similar idea to the maximum number in a sliding window 
        # put the max on the top.. opptunistrically if it works then use it
        # otherwise, if it is already out of window... pop it
        # I think this guarding value just make coding easier a bit it will never be popped 
        # thus keeping the heap always valid and at the end it will be used as the zero-y value
        # too super genius about this solution
        maxHeap = [(0, float('inf'))]
        for l, negH, r in events:

            # pos-1 is the ending position of a building... 
            # the right events is represnted by 0.. so it will never matter but it do trigger popping of other events
            # when current even position l is bigger than some buildings' ending position
            # that building should be popped 
            while maxHeap[0][1] <= l:
                # because left event is entered with r as ending-postion
                # so when right event arrives.. the build should always leave heap
                heapq.heappop(maxHeap)
            
            if negH != 0:
                heapq.heappush(maxHeap, (negH, r))
            
            if res[-1][1] != abs(maxHeap[0][0]):
                res.append([l, abs(maxHeap[0][0])])
        
        return res[1:]
            
""""
Runtime: 117 ms, faster than 96.76% of Python3 online submissions for The Skyline Problem.
Memory Usage: 20.1 MB, less than 56.95% of Python3 online submissions for The Skyline Problem.
"""




if __name__ == '__main__':
    s = Solution()
    print(s.getSkyline([[1, 15, 8], [2, 9, 10], [11, 16, 10]]))
    # print(s.getSkyline([[0,2,3],[2,5,3]]))