"""
https://leetcode.com/problems/minimum-cost-to-reach-destination-in-time/?envType=study-plan&id=graph-ii

seems not very hard?
either dfs or bfs + dp

bfs: I can track the budget,time and push it along the road
apparently, going backwards is only increasing time and fee so not 


but towards a city, there could be multiple roads
even between one and the other city, there could be >1 roads

so be prepared to relax the city.. take the smaller time? or smaller fee??
hmm....

or maybe keep all going...
because at a city.. 
 cost1, time1
 cost2, time2...

until reaching the end..
hard to say which one is better..

keep all going???
so DFS could be a little better (but again.. dfs, you can only fix on one dimension also)
dfs:
    from a city to end
        (time1, cost1), but it won't gurantee budget-time could reach this city
        (time2, cost2), could be the cost2 is higher.. but it allows the travel to finish overall

so yeah.. keep all going? but drop those over time limit
let me try 

but how to avoid cycle?
    - simply looking back
        A -> B, preventing B going back to A
    - complext looking back
        A --------> D
        |           |
        B --> C  -- |
        preventing D going back to A

        maybe, the cost>A's maxCost, time>A's maxTime
        if I keep the (time,cost) in a sortedlist?
        or maybe just care the time, if time bigger that A's maxTime, then?
            again.. at D.. maybe the 2nd route takes more time but could satisfy the fee..
            hmm... 

okay.. so I think
    say at node, it has a SortedList of (time1,cost1)..(timeK,costK)
    if it is bigger than maxTime,maxCost, then absolutely it is not needed
    if it is smaller than minTime,minCost, then it is absolutely the best and actually, we only need it

    what is says?
    it seems to say, binary search the list and get rid of later pairs where, 
        timeP,costP > the incoing ones..

        let me think if this is all enough
        let me say I use time to maintain the order 
        in the left side, all the time needed are smaller than incoming ones
        so we need to also see,if there is one that with also smaller cost.. if yes, then this one is not needed at all...
        (this part cannot binary search, O(n)?)
okay.. thinking enough.. let me start with some code and see if I figure out more
    
"""


import bisect
from collections import defaultdict, deque
import heapq
from typing import List

from sortedcontainers import SortedList


class Solution:
    def minCost(self, maxTime: int, edges: List[List[int]], passingFees: List[int]) -> int:
        graphs = defaultdict(set)
        for n1,n2,time in edges:
            graphs[n1].add((n2,time))
            graphs[n2].add((n1, time))

        n = len(passingFees)
        timeCost = [[] for _ in range(n)]

        q = deque()
        # city, time, fee
        # arriving in city, the time needed and the fee to pay
        # think enter the last city to pay fee
        q.append((0, 0, passingFees[0]))  
        minFee = float('inf')
        while q:
            city,time,fee = q.popleft()
            if time > maxTime:
                continue
            
            if city == n-1:
                minFee = min(minFee, fee)
                continue

            if len(timeCost[city]) == 0:
                # first visit to this city
                timeCost[city].append((time,fee))
            else:
                if (time,fee) >= timeCost[city][-1]:
                    # time,fee is bigger than all previous pairs
                    # looking back or cycle back.. 
                    # useless route
                    continue
                else:
                    # visit city via different routes
                    idx = bisect.bisect_left(timeCost[city], (time, fee))

                    # [idx:] is useless (because incoming pair of (time,fee) could invalidate all of them)
                    timeCost[city] = timeCost[city][:idx]

                    # [:idx] - all have smaller time
                    # check if they have smaller cost.. if yes.. this incoming one is useless
                    # useful = True
                    # for _,c in timeCost[city][::-1]:
                    #     if c<=fee:
                    #         # no need to continue from here
                    #         useful = False
                    #         break
                    # if not useful:
                    #     continue
                    # this could be totally unnecessary
                    # if timeCost[city] and timeCost[city][-1][1] <= fee:
                    #     continue

                    timeCost[city].append((time,fee))

            # now this route could be candidate. continue exploring its desendants
            for nextCity,travelTime in graphs[city]:
                if timeCost[nextCity] and (time+travelTime, fee+passingFees[nextCity]) > timeCost[nextCity][-1]:
                    continue
                q.append((nextCity, time+travelTime, fee+passingFees[nextCity]))
                
        return minFee if minFee != float('inf') else -1


"""
84 / 92 test cases passed.
and wrong answer.. hell...

where could be a bug?
element at the idx if it is equal? it could go on

should be ok.. I just replace A with A.. nothing changes.. 

I feel this is a viable solution but where it goes wrong?
to debug? that case is too big

can I think of a case myself???

okay.. taking a break to walk and quickly figured out where went wrong
its here
                    idx = bisect.bisect_left(timeCost[city], (time, fee))

                    # [idx:] is useless (because incoming pair of (time,fee) could invalidate all of them)
                    timeCost[city] = timeCost[city][:idx]
    lets say I have a list like [[1,10], [3,8], [5,6]]
    incoming is [4,7].. 
    it will land before [5,6] do I get rid of [5,6]]???? obviously not

    so I have pruned some paths too early

so what to do instead?
notice this list is ascending on time dimension but descending on fee dimension
that has to be true

if some element has time2>=time1 and cost2>=cost1.. then it is useless
so with this in mind.. the rules seem to be 
1. incoming >= sl[-1], useless
2. incoming < s[0], whole list useless
3. complexe cases
    a. bisect_left it
    b. if idx==0:
        that means timeIn < time0 or (timeIn == time0 and costIn <= cost0)
        timeIn < time0:
            if costIn > cost0, then it just becomes the head
        timeIn == time0:
            costIn < cost0, slot0 can be replaced... 
            it can replace until costK<costIn (this is complicated)
    c. if idx==len()
        that menas timeIn > time[-1] or (timeIn == time[-1] and costIn > cost[-1])
        timeIn > time[-1]:
            if costIn >= cost[-1], then it is useless -- this is actually taken care by above
            if costIn < cost[-1], the it becomes the tail
        timeIn == time[-1]:
            costIn > cost[-1], useless.. this is taken care by case 1 as well
    d. in the mid
        looking left
            either timeIn>timeLeft
                if costIn>costLeft, useless
                or could be useful
            timeIn==timeLeft and costIn>costLeft
                uselsee
        looking right
            timeIn<timeRight
                if costIn<costRight, right useless, this will continue until find a costK<costIn
            timeIn==timeRight and costIn<=costRight
                right useless, this will continue until find a costK<costIn

this is way too complicatede, rethink 
just three cases (maybe 4)

1. incoming >= sl[-1], incoming useless
2. incoming < sl[0], whole list useless

3. if the landing element is exactly same as incoming, nothing changed

4. looking right and left
    now it cannot landing on an element exactlay the same 
    so <= sl[0]  or >= s[-1] are taken care of, we can assume there is a left and right
    looking left:
        either one of following
            timeIn>timeLeft
                => costIn>=costLeft, useless
                => costIn<costLeft, could be useful (depending on right side)
            timeIn==timeLeft and costIn>costLeft
                => useless
    
    look right:
        either of following
            timeIn < timeRight
                => costIn>costRight, could be useful
                => costIn<=costRight, 
                    useful
                    right element useless.. (this continue until a costK<costIn)
            timeIn == timeRight
                => costIn<costRight (== equal case taken care)
                    right element replacement (continue..)


not super easy to code it up
but give a try

okay.. not right yet for case 1&2
remember the time is increasing but fee is decreasing 

so 
case 1: incoming >= sl[-1], continue to hold true
case 2: incoming < sl[0], this should walk up to that costK < costIn
case 3: same
case 4: no change
    case 2 is included by case 4 

"""


class Solution:
    def minCost(self, maxTime: int, edges: List[List[int]], passingFees: List[int]) -> int:
        graphs = defaultdict(set)
        for n1, n2, time in edges:
            graphs[n1].add((n2, time))
            graphs[n2].add((n1, time))

        n = len(passingFees)
        timeCost = [[] for _ in range(n)]

        q = deque()
        # city, time, fee
        # arriving in city, the time needed and the fee to pay
        # think enter the last city to pay fee
        q.append((0, 0, passingFees[0]))
        minFee = float('inf')
        while q:
            city, time, fee = q.popleft()
            if time > maxTime:
                continue

            if city == n-1:
                minFee = min(minFee, fee)
                continue

            if len(timeCost[city]) == 0:
                # first visit to this city
                timeCost[city].append((time, fee))
            else:
                if (time, fee) >= timeCost[city][-1]:
                    # case 1
                    # time,fee is bigger than all previous pairs
                    # looking back or cycle back..
                    # useless route
                    continue
                else:
                    # visit city via different routes
                    idx = bisect.bisect_left(timeCost[city], (time, fee))
                    if timeCost[city][idx] == (time,fee):
                        # case 3:
                        continue

                    # case 4 (2):
                    newList = list(timeCost[city])
                    useless = False
                    if idx:
                        # looking left if idx>0
                        timeLeft, costLeft = timeCost[city][idx-1]
                        if (time > timeLeft and fee >= costLeft) or (time==timeLeft and fee > costLeft):
                            useless = True

                    if not useless:
                        # if it useless looking left
                        # that means it has been invalidated.. no need to look right
                        # now it is useful.. 
                        if idx < len(timeCost[city]):
                            # looking right if idx<len()
                            timeRight, costRight = timeCost[city][idx]
                            if time == timeRight and fee < costRight:
                                # replace idx element and could invalidate later elements 
                                newList[idx] = (time,fee)
                                idx2 = idx+1
                                while idx2 < len(timeCost[city]) and timeCost[city][idx2][1]>=fee:
                                    idx2+=1
                                newList[idx+1:] = timeCost[city][idx2:]
                            elif time < timeRight:
                                if fee > costRight:
                                    # just insert at idx and copy previous 
                                    newList[idx] = (time, fee)
                                    newList[idx+1:] = timeCost[city][idx:]
                                else:
                                    # replace idx
                                    newList[idx] = (time, fee)
                                    idx2 = idx+1
                                    while idx2 < len(timeCost[city]) and timeCost[city][idx2][1]>=fee:
                                        idx2+=1
                                    newList[idx+1:] = timeCost[city][idx2:]
                    timeCost[city] = newList

            # now this route could be candidate. continue exploring its desendants
            for nextCity, travelTime in graphs[city]:
                if timeCost[nextCity] and (time+travelTime, fee+passingFees[nextCity]) > timeCost[nextCity][-1]:
                    continue
                q.append((nextCity, time+travelTime,
                         fee+passingFees[nextCity]))

        return minFee if minFee != float('inf') else -1


"""
okay.. this is taking too long.. 

okay.. still wrong answer.. 
I am total failure today..



"""


class Solution:
    def minCost(self, maxTime: int, edges: List[List[int]], passingFees: List[int]) -> int:
        graphs = defaultdict(set)
        for n1, n2, time in edges:
            graphs[n1].add((n2, time))
            graphs[n2].add((n1, time))

        n = len(passingFees)
        timeCost = [[] for _ in range(n)]

        q = deque()
        # city, time, fee
        # arriving in city, the time needed and the fee to pay
        # think enter the last city to pay fee
        q.append((0, 0, passingFees[0]))
        minFee = float('inf')
        while q:
            city, time, fee = q.popleft()
            print(city, timeCost[city], time,fee, minFee)
            if city == 49:
                breaker = 1
            # print(minFee, city, time, fee)
            if time > maxTime or fee >= minFee:
                continue

            if city == n-1:
                minFee = min(minFee, fee)
                continue
            
            
            if len(timeCost[city]) == 0:
                # first visit to this city
                timeCost[city].append((time, fee))
            else:
                if (time, fee) >= timeCost[city][-1]:
                    # case 1
                    # time,fee is bigger than all previous pairs
                    # looking back or cycle back..
                    # useless route
                    continue
                else:
                    # visit city via different routes
                    
                    idx = bisect.bisect_left(timeCost[city], (time, fee))
                    if timeCost[city][idx] == (time, fee):
                        # case 3:
                        continue

                    # case 4 (2):
                    
                    useless = False
                    if idx:
                        # looking left if idx>0
                        timeLeft, costLeft = timeCost[city][idx-1]
                        if (time > timeLeft and fee >= costLeft) or (time == timeLeft and fee > costLeft):
                            useless = True

                    if not useless:
                        # if it useless looking left
                        # that means it has been invalidated.. no need to look right
                        # now it is useful..
                        if idx < len(timeCost[city]):
                            # looking right if idx<len()
                            timeRight, costRight = timeCost[city][idx]
                            if (time == timeRight and fee < costRight) or (time<timeRight and fee<=costRight):
                                # replace idx element and could invalidate later elements
                                timeCost[city][idx] = (time, fee)
                                idx2 = idx+1
                                # idx2 = idx+1
                                # while idx2 < len(timeCost[city]) and timeCost[city][idx2][1] >= fee:
                                #     idx2 += 1

                                # can replace this ^ with a binary search
                                # l=idx+1
                                # r=len(timeCost[city])
                                # while l<r:
                                #     m = l+(r-l)//2
                                #     if timeCost[city][m][1] >= fee:
                                #         l = m+1
                                #     else:
                                #         r = m
                                # idx2 = l

                                timeCost[city][idx+1:] = timeCost[city][idx2:]
                            elif time < timeRight:
                                if fee > costRight:
                                    # just insert at idx -- this could the most time consuming place?
                                    timeCost[city][idx:idx] = [(time,fee)]
                            else:
                                print('useless')
                    else:
                        print('useless')
            print(city, timeCost[city])
                                    
            # now this route could be candidate. continue exploring its desendants
            for nextCity, travelTime in graphs[city]:
                q.append((nextCity, time+travelTime,
                         fee+passingFees[nextCity]))

        return minFee if minFee != float('inf') else -1



"""
fail and painful.. wasted a whole morning
I must go to system design for afternoon...

today is no progress...
it is supposed to happen...

okay.. on the way out
I think of following

just use heap.. 
put the time into the heap

and use that maxTime and ever learn minFee to terminate early..
"""


class Solution:
    def minCost(self, maxTime: int, edges: List[List[int]], passingFees: List[int]) -> int:
        graphs = defaultdict(set)
        for n1, n2, time in edges:
            graphs[n1].add((n2, time))
            graphs[n2].add((n1, time))

        n = len(passingFees)
        h = []
        heapq.heappush(h, (0, passingFees[0], 0)) # time, cost, city
        minFee = float('inf')
        
        minFeePerCity = [float('inf') ]*n

        while h:
            time, fee, city = heapq.heappop(h)

            if time>maxTime or fee >= minFee:
                continue
            
            if city == n-1:
                minFee = min(minFee, fee)
                continue

            # by here, time factor is consider above? so only need to focus on the fee dimension
            if minFeePerCity[city] < fee:
                continue
            minFeePerCity[city] = fee
                
            for nextCity,travelTime in graphs[city]:
                heapq.heappush(h, (time+travelTime, fee + passingFees[nextCity], nextCity))
        
        return minFee if minFee != float('inf') else -1

            
"""
Runtime: 790 ms, faster than 47.18% of Python3 online submissions for Minimum Cost to Reach Destination in Time.
Memory Usage: 15 MB, less than 34.51% of Python3 online submissions for Minimum Cost to Reach Destination in Time.

hmm..

I see most folks sort on fees then record time and do that 
I guess that is just equavilent to what I did
"""


class Solution:
    def minCost(self, maxTime: int, edges: List[List[int]], passingFees: List[int]) -> int:
        graphs = defaultdict(set)
        for n1, n2, time in edges:
            graphs[n1].add((n2, time))
            graphs[n2].add((n1, time))

        n = len(passingFees)
        h = []
        heapq.heappush(h, (passingFees[0], 0, 0))  # cost, time, city
        minFee = float('inf')

        minTimePerCity = [float('inf')]*n

        while h:
            fee,time, city = heapq.heappop(h)

            if time > maxTime or fee >= minFee:
                continue

            if city == n-1:
                return fee

            if minTimePerCity[city] > time:
                # I think this means..
                # possible a better route appeas.. 
                # anyway.. it is a min() aggregation..
                # so indeed I over-complicated things
                minTimePerCity[city] = time
                for nextCity, travelTime in graphs[city]:
                    heapq.heappush(h, ( fee +passingFees[nextCity], time+travelTime,nextCity))

        return -1

"""
Runtime: 558 ms, faster than 66.90% of Python3 online submissions for Minimum Cost to Reach Destination in Time.
Memory Usage: 15.1 MB, less than 14.79% of Python3 online submissions for Minimum Cost to Reach Destination in Time.

"""


class Solution:
    def minCost(self, maxTime: int, edges: List[List[int]], passingFees: List[int]) -> int:
        graphs = defaultdict(set)
        for n1, n2, time in edges:
            graphs[n1].add((n2, time))
            graphs[n2].add((n1, time))

        n = len(passingFees)
        h = []
        heapq.heappush(h, (0, passingFees[0], 0))  # time, cost, city
        minFee = float('inf')

        minFeePerCity = [float('inf')]*n

        while h:
            time, fee, city = heapq.heappop(h)

            if time > maxTime or fee >= minFee:
                continue

            if city == n-1:
                minFee = min(minFee, fee)
                continue

            # by here, time factor is consider above? so only need to focus on the fee dimension
            if minFeePerCity[city] > fee:  
                # because its aggregation
                # only to consider all the candidates
                # as for their order.. not that important?
                minFeePerCity[city] = fee
                for nextCity, travelTime in graphs[city]:
                    heapq.heappush(h, (time+travelTime, fee +
                                passingFees[nextCity], nextCity))

        return minFee if minFee != float('inf') else -1

"""
same structure but on time 

but if you don't heapify on cost.. but heapify on time..
when it reaches end.. it could be sub-optimal indeed... 

if you heapify on cost.. that is naturally guranteed... how interesting!

Runtime: 753 ms, faster than 50.00% of Python3 online submissions for Minimum Cost to Reach Destination in Time.
Memory Usage: 15.1 MB, less than 19.01% of Python3 online submissions for Minimum Cost to Reach Destination in Time.

very hard to spot the hariline defect in my above logic

I think I was trying to control two moving dimensions 
while the better way is 
    - focus on one (time or cost)
    - try all of them
    - this is aggregation (min)
    - early termination
"""

if __name__ == '__main__':
    s = Solution()
    print(s.minCost(maxTime = 30, edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]], passingFees = [5,1,2,20,20,3]))
    print(s.minCost(maxTime = 29, edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]], passingFees = [5,1,2,20,20,3]))
    print(s.minCost(maxTime = 25, edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]], passingFees = [5,1,2,20,20,3]))
    print(s.minCost(maxTime=123, edges=[[0, 1, 10], [1, 2, 12], [2, 5, 10], [
          0, 3, 1], [3, 4, 123], [4, 5, 15]], passingFees=[5, 12, 2, 20, 20, 3]))

    maxTime = 500
    edges = [[9,7,18],[26,3,12],[28,45,33],[47,10,27],[34,18,38],[32,13,39],[32,26,32],[12,0,2],[4,1,7],[5,3,2],[39,25,27],[45,10,34],[3,19,5],[25,32,23],[30,10,47],[37,2,31],[10,32,15],[23,14,19],[22,6,14],[45,39,38],[39,21,30],[42,17,42],[20,17,15],[24,0,27],[2,46,11],[2,24,13],[36,22,30],[2,1,31],[41,35,45],[4,19,20],[32,27,33],[38,46,1],[21,11,15],[33,41,2],[45,18,30],[8,33,50],[37,11,6],[25,17,42],[45,39,33],[7,4,49],[17,42,36],[36,16,9],[46,25,24],[43,4,6],[35,13,28],[1,28,1],[34,35,15],[38,1,15],[16,6,28],[13,0,42],[3,30,24],[43,27,35],[8,0,45],[27,20,47],[6,16,47],[0,34,35],[0,35,3],[40,11,24],[1,0,49],[44,20,32],[26,12,17],[3,2,25],[37,25,42],[27,1,15],[36,25,38],[24,47,33],[33,28,15],[25,43,37],[47,31,47],[29,10,50],[11,1,21],[29,3,48],[1,25,10],[48,17,16],[19,24,22],[30,7,2],[11,22,19],[20,42,41],[27,3,48],[17,0,34],[19,14,32],[49,2,20],[10,3,38],[0,49,13],[6,3,28],[42,23,6],[14,8,1],[35,16,3],[17,7,40],[18,7,49],[36,35,13],[14,40,45],[16,33,11],[31,22,33],[38,15,48],[15,14,25],[37,13,37],[44,32,7],[48,1,31],[33,12,20],[22,26,23],[4,10,11],[43,28,43],[19,8,14],[35,31,33],[28,27,19],[40,11,36],[36,43,28],[22,21,15]]
    passFees = [199,505,107,961,682,400,304,517,512,18,334,627,893,412,922,289,19,161,206,879,336,831,577,802,139,348,440,219,273,691,99,858,389,955,561,353,937,904,858,704,548,497,787,546,241,67,743,42,87,137]

    print(s.minCost(maxTime, edges, passFees))

    maxTime = 500
    edges = [[31,36,19],[5,19,32],[2,17,40],[13,25,4],[9,18,31],[10,40,19],[34,43,46],[7,44,42],[7,37,2],[37,44,43],[27,9,36],[20,31,44],[36,25,16],[20,49,31],[17,13,18],[30,13,25],[18,22,50],[1,0,44],[15,19,21],[14,38,48],[31,11,31],[43,9,2],[6,34,25],[38,23,3],[42,8,12],[47,29,18],[15,49,1],[40,11,26],[48,11,39],[32,30,37],[34,26,16],[46,22,15],[14,34,45],[15,22,42],[35,13,31],[5,4,46],[12,27,5],[13,27,16],[49,13,2],[7,42,42],[46,9,5],[2,40,24],[20,16,9],[10,11,25],[17,22,50],[42,23,27],[41,42,35],[13,39,10],[28,11,36],[47,3,33],[24,42,50],[26,29,22],[48,7,33],[42,39,25],[33,8,46],[45,43,20],[43,20,39],[6,27,4],[4,6,50],[49,11,15],[30,44,21],[30,19,5],[3,11,34],[41,7,16],[37,33,9],[2,1,21],[5,46,7],[10,32,14],[4,43,12],[37,27,40],[6,8,15],[1,23,9],[1,15,43],[20,34,41],[17,11,50],[39,48,4],[46,9,11],[24,0,3],[21,9,17],[32,30,39],[37,4,32],[16,14,12],[35,42,18],[26,17,50],[7,37,9],[45,37,22],[30,29,42],[7,34,47],[9,29,7],[43,24,6],[13,18,15],[10,34,11],[45,8,18],[45,1,5],[17,9,28],[37,35,18],[42,15,5],[37,6,26],[0,14,49],[12,44,33],[35,45,21],[21,26,2],[32,42,26],[36,48,26],[35,7,50],[9,15,16],[4,2,11],[47,45,29],[41,4,13],[38,25,31],[10,38,9],[23,41,23],[9,37,10],[29,18,38],[45,25,25],[22,20,26],[28,9,15],[41,40,32],[24,8,19],[25,0,25],[6,28,46],[8,35,46],[25,7,46],[21,11,37],[14,28,21],[3,1,24],[33,24,31],[24,26,7],[39,47,31],[0,24,36],[21,48,24],[37,7,3],[15,46,3],[24,20,49],[5,39,17],[8,1,23],[3,28,42],[1,19,30],[41,22,39],[34,39,15],[13,28,19],[28,21,48],[7,3,13],[23,48,36],[5,8,19],[25,0,35],[25,22,48],[2,37,33],[2,33,13],[40,5,35],[13,45,30],[1,18,40],[2,39,12],[23,8,20],[3,22,8],[6,43,21],[11,3,24],[3,47,47],[10,19,37],[20,23,14],[7,0,39],[10,3,40],[34,27,29],[29,25,46],[22,33,48],[11,47,40],[10,15,35],[42,39,28],[37,23,4],[37,5,1],[48,2,32],[13,5,33],[49,11,35],[27,0,20],[41,7,23],[1,35,4],[9,22,9],[20,25,45],[19,47,46],[11,12,15],[42,18,49],[19,1,5],[28,23,48],[42,4,36],[48,12,11],[32,44,2],[49,39,15],[45,39,34],[11,8,1],[26,43,36],[32,31,39],[49,42,47],[9,13,24],[30,40,2],[17,32,12],[35,40,22],[43,2,13],[23,32,23],[48,22,13],[6,24,4],[48,5,41],[18,3,5],[46,37,21],[13,29,42],[22,44,37],[3,24,6],[21,4,42],[37,32,8],[38,42,27],[30,1,28],[6,21,22],[33,21,38],[12,42,47],[13,32,33],[35,33,20],[37,1,33],[27,39,14],[10,9,1],[40,45,48],[6,32,9],[30,44,16],[36,42,20],[11,32,23],[16,19,1],[21,11,39],[45,9,23],[11,48,22],[33,23,38],[8,45,1],[40,33,28],[30,10,18],[5,25,33],[34,4,16],[34,21,22],[35,22,9],[34,7,35],[4,9,43],[48,25,36],[34,4,36],[13,12,11],[49,46,40],[49,34,41],[32,27,16],[25,41,39],[22,6,26],[34,0,11],[42,11,22],[40,14,16],[23,19,19],[4,36,26],[23,48,29],[38,32,13],[16,33,28],[46,23,23],[2,47,19],[13,6,48],[10,31,24],[17,2,41],[33,37,3],[17,39,31],[32,28,14],[3,7,28],[45,4,50],[43,33,20],[35,45,28],[41,47,17],[36,25,8],[32,40,6],[27,24,46],[11,29,50],[9,7,29],[11,30,29],[37,16,47],[19,12,39],[36,41,20],[15,44,32],[13,0,44],[23,26,26],[23,20,26],[38,8,44],[15,5,48],[11,0,25],[32,15,40],[30,32,2],[35,2,46],[32,6,11],[39,3,40],[20,9,39],[9,10,15],[45,14,7],[20,32,27],[36,33,46],[27,0,23],[7,25,22],[25,40,3],[22,3,38],[44,42,46],[16,35,3],[5,32,20],[34,12,50],[43,9,44],[28,21,33],[34,47,4],[38,34,17],[23,49,4],[24,27,4],[30,3,36],[1,41,5],[38,20,37],[9,6,45],[32,19,14],[15,21,22],[42,40,37],[21,32,32],[4,2,34],[30,2,34],[39,12,15],[46,17,30],[47,22,5],[20,31,45],[21,48,46],[49,34,36],[29,32,36],[37,39,45],[17,13,15],[39,3,37],[12,38,16],[23,32,18],[0,9,9],[4,19,37],[25,24,27],[44,39,42],[37,32,31],[45,5,22],[47,36,42],[32,6,9],[31,30,1],[37,41,19],[12,10,9],[10,21,9],[35,1,30],[23,21,17],[33,10,37],[21,10,37],[27,45,16],[23,22,45],[9,43,21],[13,24,43],[44,36,29],[18,36,40],[2,39,16],[33,8,3],[23,13,4],[24,42,33],[18,11,27],[9,8,11],[34,22,11],[44,30,22],[23,6,7],[48,42,45],[20,21,19],[21,3,31],[41,12,39],[23,42,38],[5,39,32],[37,31,3],[23,12,15],[27,16,49],[30,35,3],[41,46,37],[44,18,27],[17,36,30],[1,36,12],[34,9,15],[10,17,27],[23,27,36],[36,42,36],[38,46,45],[46,9,4],[28,36,7],[9,24,28],[49,48,33],[9,18,2],[17,26,9],[30,34,39],[18,11,7],[37,27,6],[16,39,4],[33,1,37],[12,48,37],[26,14,39],[4,42,42],[35,46,42],[28,31,25],[48,24,27],[37,13,19],[20,21,20],[34,30,37],[31,7,33],[48,49,5],[5,30,22],[9,4,43],[33,15,7],[27,35,20],[12,5,41],[14,4,40],[44,11,49],[35,6,42],[26,12,45],[3,1,48],[28,31,11],[10,8,29],[14,18,45],[7,4,14],[14,8,7],[17,34,20],[29,41,41],[3,0,3],[29,18,1],[41,5,9],[5,28,13],[49,21,38],[16,13,39],[19,10,34],[39,32,20],[26,29,24],[31,34,19],[23,31,42],[13,25,47],[27,15,32],[15,31,33],[31,11,29],[40,27,27],[16,22,25],[22,1,42],[31,2,11],[31,4,33],[6,3,21],[11,39,29],[15,7,2],[22,6,13],[10,42,43],[37,15,48],[4,38,50],[20,34,24],[33,19,15],[42,26,26],[37,35,34],[22,23,24],[7,27,10],[6,4,44],[11,14,20],[8,2,18],[25,44,25],[42,15,44],[24,26,34],[12,3,24],[28,34,29],[24,30,2],[1,39,1],[6,3,26],[38,11,13],[46,23,1],[2,46,41],[32,40,43],[48,40,15],[17,39,5],[25,34,8],[42,38,2],[25,28,10],[37,20,28],[29,2,29],[43,21,29],[25,17,23],[27,23,36],[15,40,41],[20,1,12],[0,16,49],[35,32,15],[14,42,12],[45,13,4],[36,8,36],[1,13,21],[28,12,12],[41,32,48],[22,28,7],[29,47,31],[26,4,17],[37,11,21],[39,12,35],[5,33,12],[20,14,4],[2,33,47],[16,14,13],[30,34,3],[33,29,13],[40,15,17],[32,24,34],[38,22,17],[5,26,10],[45,31,26],[19,5,29],[20,14,21],[34,19,9],[19,41,38],[46,19,48],[11,20,10],[34,4,16],[1,29,26],[5,46,24],[16,15,14],[29,8,45],[44,19,3],[21,3,30],[43,47,37],[17,31,7],[43,39,20],[44,40,10],[31,45,29],[5,1,25],[12,17,19],[14,18,46],[15,35,45],[48,11,14],[7,2,8],[28,34,4],[41,30,43],[22,29,49],[23,16,20],[41,22,48],[19,37,48],[12,20,23],[23,21,42],[25,34,28],[17,46,27],[20,26,8],[2,46,13],[28,2,22],[47,21,44],[15,27,11],[33,6,17],[44,15,41],[20,10,18],[46,15,14],[32,10,9],[25,49,30],[15,44,50],[41,24,23],[29,22,15],[25,29,40],[36,44,13],[8,9,1],[48,9,9],[13,12,5],[45,18,7],[31,1,7],[28,14,18],[20,42,48],[3,20,11],[30,4,49],[29,8,37],[30,46,37],[38,16,44],[7,36,42],[0,45,8],[20,38,8],[28,32,27],[1,41,45],[8,28,26],[32,34,39],[12,31,18],[26,4,34],[37,3,14],[17,33,13],[34,21,16],[46,16,49],[38,39,41],[20,24,14],[38,21,15],[28,10,38],[35,20,18],[29,4,13],[30,3,48],[35,10,45],[2,23,37],[3,23,32],[3,6,39],[36,31,18],[37,6,40],[28,15,45],[24,42,31],[16,19,32],[9,31,8],[46,35,48],[0,2,28],[26,0,19],[36,14,40],[7,11,25],[3,49,21],[36,33,1],[43,8,38],[46,20,29],[35,37,30],[49,28,39],[38,48,3],[23,9,17],[4,49,28],[44,33,18],[6,17,47],[25,29,8],[3,27,47],[36,17,12],[25,34,14],[30,23,2],[8,40,7],[25,3,38],[44,0,47],[37,12,38],[5,28,42],[36,2,46],[5,39,16],[7,27,41],[26,47,11],[27,23,15],[4,8,50],[14,11,20],[32,9,21],[2,0,31],[41,17,47],[29,9,24],[4,37,35],[43,44,14],[27,8,22],[47,2,28],[19,24,1],[40,0,1],[29,21,40],[7,5,48],[0,21,8],[18,9,10],[36,0,13],[12,27,29]]
    passFees = [274,630,138,293,592,832,255,72,877,611,272,59,956,23,443,626,989,290,864,487,433,447,861,829,70,190,220,787,696,35,954,653,844,776,440,977,870,425,364,964,364,524,933,152,184,809,232,235,830,965]
    print(s.minCost(maxTime, edges, passFees))
    maxTime = 119
    edges = [[9,18,2],[1,35,4],[24,26,34],[2,47,19],[15,31,33],[21,10,37],[35,33,20],[32,15,40],[13,5,33],[28,34,4],[31,11,31],[17,34,20],[49,48,33],[37,35,34],[21,26,2],[42,11,22],[15,49,1],[4,36,26],[32,31,39],[37,23,4],[32,34,39],[2,46,13],[34,19,9],[11,14,20],[34,12,50],[43,8,38],[24,8,19],[3,28,42],[38,8,44],[10,34,11],[37,1,33],[28,31,11],[4,42,42],[23,13,4],[12,27,29],[33,6,17],[32,27,16],[26,29,24],[26,14,39],[36,42,36],[17,22,50],[9,6,45],[48,24,27],[45,9,23],[49,42,47],[3,27,47],[38,46,45],[4,2,11],[33,23,38],[14,38,48],[46,20,29],[30,13,25],[5,30,22],[6,32,9],[37,15,48],[27,0,23],[37,44,43],[21,11,39],[36,25,8],[31,30,1],[27,39,14],[11,0,25],[31,1,7],[9,29,7],[15,44,32],[44,39,42],[22,1,42],[3,6,39],[41,32,48],[28,10,38],[19,47,46],[16,14,13],[29,8,37],[48,12,11],[37,41,19],[6,21,22],[25,34,8],[30,29,42],[30,35,3],[7,3,13],[48,22,13],[49,34,41],[7,0,39],[48,42,45],[44,42,46],[2,39,12],[19,10,34],[28,21,48],[42,39,28],[13,12,11],[1,36,12],[6,43,21],[13,6,48],[2,46,41],[10,15,35],[46,9,5],[35,45,21],[37,27,6],[23,20,26],[36,31,18],[2,40,24],[42,40,37],[13,29,42],[41,7,16],[48,40,15],[20,23,14],[46,15,14],[38,32,13],[23,9,17],[24,30,2],[21,32,32],[39,3,37],[35,6,42],[5,28,13],[38,11,13],[31,7,33],[11,20,10],[34,27,29],[6,3,21],[2,17,40],[41,22,48],[14,28,21],[42,38,2],[3,47,47],[36,33,1],[20,31,45],[34,22,11],[5,39,16],[39,32,20],[35,13,31],[4,8,50],[29,22,15],[29,2,29],[11,47,40],[39,48,4],[33,21,38],[25,0,35],[15,19,21],[44,11,49],[28,23,48],[10,38,9],[49,34,36],[1,39,1],[22,6,13],[40,27,27],[34,26,16],[9,10,15],[11,12,15],[33,29,13],[20,25,45],[41,22,39],[24,42,33],[12,3,24],[9,37,10],[10,32,14],[5,26,10],[20,49,31],[33,37,3],[25,0,25],[17,11,50],[22,33,48],[14,11,20],[26,47,11],[13,32,33],[12,27,5],[20,32,27],[28,15,45],[37,27,40],[1,29,26],[30,44,16],[20,34,41],[41,17,47],[32,24,34],[41,42,35],[9,15,16],[30,34,3],[15,27,11],[34,4,36],[8,9,1],[12,31,18],[38,42,27],[22,28,7],[18,22,50],[41,40,32],[24,26,7],[41,4,13],[7,44,42],[25,49,30],[8,28,26],[25,7,46],[11,3,24],[32,40,6],[24,0,3],[20,26,8],[41,24,23],[44,0,47],[6,17,47],[4,6,50],[25,34,14],[46,35,48],[43,33,20],[46,19,48],[40,15,17],[6,4,44],[38,23,3],[6,8,15],[17,13,15],[2,0,31],[45,31,26],[5,1,25],[46,17,30],[5,46,24],[42,15,44],[16,14,12],[23,48,36],[30,23,2],[11,48,22],[27,8,22],[30,32,2],[46,23,1],[26,43,36],[5,39,32],[23,27,36],[44,18,27],[9,43,21],[25,34,28],[4,38,50],[23,21,42],[38,39,41],[35,45,28],[8,1,23],[6,27,4],[30,44,21],[37,4,32],[44,36,29],[23,32,23],[47,3,33],[34,39,15],[37,32,31],[9,22,9],[2,23,37],[10,31,24],[11,8,1],[33,15,7],[40,11,26],[33,8,46],[1,41,5],[45,13,4],[15,40,41],[7,4,14],[28,9,15],[23,49,4],[15,22,42],[13,39,10],[4,19,37],[34,21,22],[2,33,13],[1,18,40],[17,46,27],[44,15,41],[3,20,11],[13,0,44],[15,44,50],[20,24,14],[49,39,15],[27,45,16],[5,8,19],[2,39,16],[37,20,28],[49,28,39],[39,12,15],[23,41,23],[1,19,30],[25,41,39],[25,17,23],[46,9,4],[37,11,21],[21,9,17],[30,10,18],[35,2,46],[10,19,37],[17,32,12],[26,4,34],[8,35,46],[10,42,43],[23,21,17],[29,47,31],[29,4,13],[18,36,40],[27,15,32],[20,14,4],[23,22,45],[37,5,1],[12,20,23],[37,32,8],[22,20,26],[12,48,37],[14,42,12],[14,8,7],[0,14,49],[37,39,45],[15,46,3],[17,13,18],[30,34,39],[23,8,20],[12,17,19],[29,21,40],[48,11,39],[37,7,3],[34,7,35],[20,9,39],[6,3,26],[11,29,50],[21,3,30],[33,24,31],[2,1,21],[22,3,38],[34,21,16],[7,42,42],[27,16,49],[23,12,15],[16,22,25],[27,23,15],[48,7,33],[14,18,45],[45,4,50],[7,36,42],[16,19,1],[16,35,3],[48,25,36],[10,8,29],[37,13,19],[36,41,20],[8,40,7],[35,32,15],[30,4,49],[7,27,41],[35,1,30],[38,48,3],[37,33,9],[48,5,41],[44,30,22],[9,7,29],[21,3,31],[0,45,8],[0,9,9],[48,49,5],[17,39,31],[29,18,1],[22,44,37],[18,9,10],[17,39,5],[13,25,47],[12,38,16],[38,25,31],[27,24,46],[35,20,18],[0,24,36],[42,8,12],[19,12,39],[45,43,20],[47,2,28],[22,29,49],[11,30,29],[36,25,16],[43,24,6],[32,40,43],[34,4,16],[14,18,46],[20,21,19],[41,30,43],[38,34,17],[10,17,27],[21,48,24],[21,4,42],[35,37,30],[8,45,1],[43,20,39],[10,11,25],[35,46,42],[27,35,20],[4,2,34],[43,44,14],[16,15,14],[9,24,28],[29,8,45],[40,0,1],[10,21,9],[4,9,43],[3,7,28],[48,11,14],[3,24,6],[28,11,36],[1,41,45],[45,1,5],[32,9,21],[15,7,2],[3,49,21],[13,12,5],[36,14,40],[11,39,29],[45,37,22],[41,5,9],[49,11,15],[46,22,15],[1,23,9],[10,40,19],[33,1,37],[31,45,29],[39,47,31],[28,2,22],[43,9,44],[30,3,48],[29,32,36],[5,39,17],[26,4,17],[18,3,5],[24,20,49],[33,8,3],[20,1,12],[46,9,11],[2,37,33],[27,0,20],[30,3,36],[5,4,46],[3,1,24],[22,23,24],[35,10,45],[45,8,18],[38,16,44],[48,9,9],[34,0,11],[46,23,23],[28,21,33],[9,8,11],[47,29,18],[38,22,17],[46,37,21],[7,5,48],[16,39,4],[49,46,40],[27,9,36],[17,33,13],[47,22,5],[5,46,7],[20,16,9],[27,23,36],[9,4,43],[47,36,42],[6,28,46],[31,4,33],[34,43,46],[18,11,7],[29,25,46],[36,33,46],[42,15,5],[49,13,2],[20,38,8],[37,31,3],[32,44,2],[31,11,29],[9,18,31],[1,15,43],[28,36,7],[40,5,35],[13,24,43],[37,12,38],[12,44,33],[34,9,15],[16,19,32],[42,4,36],[37,3,14],[19,1,5],[31,2,11],[4,49,28],[23,31,42],[17,9,28],[32,19,14],[29,9,24],[15,21,22],[36,8,36],[9,31,8],[37,16,47],[32,30,37],[26,0,19],[20,21,20],[47,21,44],[43,47,37],[5,28,42],[7,37,9],[40,45,48],[24,27,4],[1,13,21],[36,48,26],[3,11,34],[25,29,8],[23,48,29],[37,35,18],[37,6,26],[25,22,48],[23,32,18],[33,10,37],[25,24,27],[17,36,30],[25,40,3],[23,16,20],[0,2,28],[19,24,1],[14,4,40],[17,31,7],[38,21,15],[45,14,7],[32,28,14],[12,5,41],[33,19,15],[19,5,29],[29,41,41],[43,2,13],[37,6,40],[7,11,25],[19,41,38],[43,39,20],[8,2,18],[34,30,37],[24,42,31],[42,39,25],[40,33,28],[3,22,8],[11,32,23],[7,2,8],[45,25,25],[28,12,12],[21,11,37],[28,32,27],[0,21,8],[36,0,13],[25,3,38],[13,18,15],[45,18,7],[47,45,29],[15,35,45],[17,26,9],[34,4,16],[41,12,39],[28,31,25],[41,7,23],[13,25,4],[43,9,2],[49,11,35],[1,0,44],[30,2,34],[28,34,29],[36,17,12],[3,0,3],[16,13,39],[21,48,46],[14,34,45],[9,13,24],[46,16,49],[25,29,40],[7,34,47],[20,14,21],[4,43,12],[19,37,48],[35,40,22],[44,19,3],[20,34,24],[5,33,12],[35,22,9],[7,37,2],[7,27,10],[20,10,18],[42,26,26],[15,5,48],[44,40,10],[45,39,34],[3,1,48],[39,3,40],[25,44,25],[39,12,35],[2,33,47],[13,28,19],[43,21,29],[26,12,45],[32,30,39],[6,24,4],[48,2,32],[26,29,22],[4,37,35],[12,42,47],[10,9,1],[0,16,49],[5,32,20],[40,14,16],[3,23,32],[23,19,19],[23,42,38],[41,47,17],[35,7,50],[20,31,44],[36,42,20],[45,5,22],[30,46,37],[28,14,18],[13,27,16],[24,42,50],[13,45,30],[42,23,27],[23,6,7],[38,20,37],[6,34,25],[30,1,28],[16,33,28],[26,17,50],[25,28,10],[29,18,38],[7,25,22],[20,42,48],[36,2,46],[34,47,4],[10,3,40],[5,19,32],[32,10,9],[32,6,11],[32,6,9],[5,25,33],[36,44,13],[44,33,18],[35,42,18],[17,2,41],[42,18,49],[41,46,37],[23,26,26],[30,19,5],[22,6,26],[32,42,26],[49,21,38],[12,10,9],[18,11,27],[30,40,2],[31,34,19],[31,36,19]]
    passFees = [73,745,752,321,138,703,619,28,645,724,388,653,58,298,354,790,674,885,954,928,18,712,636,450,325,599,11,781,546,324,942,905,747,806,402,712,968,778,750,53,598,833,700,458,875,703,707,667,100,434]
    print(s.minCost(maxTime, edges, passFees))
