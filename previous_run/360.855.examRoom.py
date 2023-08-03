"""
https://leetcode.com/problems/exam-room/?envType=study-plan&id=programming-skills-iii

so now my thoughts are like
for first 2 seats, it is fixed, 0 and n -1
then it works by range

the seat if offered by best range, which is provided by keep something in sorted order

(maxDist-it-can-off, start, end)
start is the tie breaker to make sure it is the lowest 

once a seat is taken, it breaks the range into two ranges..

so heap? or BST?

heap.. problem is when someone leaves.. the range combins but the old ranges are still inside there however won't impact the results?
BST or sortedlist, we can remove that two ranges... 

think heap could do the job.. keeping them in there but each time check if the sear they offer are taken or not?
if taken, split them again and rep-push...

hmm..?
just some feelings... 

"""

""""
A Total Failure... 

Why cannot I learn some lessons??? Don't waste your life on this thing!

Delete all the code to prevent me putting more time into debugging the hellish code again
tomororw I can try sorted list and remove the keys 

this is the 2nd day:
okay.. the difficulty really comes from the edge cases - the start and end seats
it is hard to deal with them generally

I have thought some more.. but still hard
then I think why not I specialize it.. if I can not generalize lets specialize
there are at most two seats of such
"""


import heapq

from sortedcontainers import SortedList


class ExamRoom:

    def __init__(self, n: int):
        self.taken = {} # any mid seats taken? and their left and right
        self.midSeats = [] # max heap: (-dist, left, right)
        self.firstSeatTaken = False # taken? and the first right seat taken
        self.lastSeatTaken = False # taken? and the first left seat taken 
        self.cap = n
        self.firstMidSeat = -1
        self.lastMidSeat = -1


    def seat(self) -> int:

        if not self.taken:
            if not self.firstSeatTaken:
                self.firstSeatTaken = True
                return 0
            elif not self.lastSeatTaken:
                self.lastSeatTaken = True
                return self.cap-1
            else:
                # first mid seat taken
                pos = (self.cap-1)//2
                self.taken[pos] = [0, self.cap-1]
                heapq.heappush(self.midSeats, [pos//2*-1, 0, pos])
                heapq.heappush(self.midSeats, [(self.cap-1-pos)//2*-1, pos, self.cap-1])
                self.firstMidSeat = self.lastMidSeat = pos
                return pos
            
        # some mid seats are taken
        leftDist = self.firstMidSeat if not self.firstSeatTaken else 0
        rightDist = self.cap - 1 - self.lastMidSeat if not self.lastSeatTaken else 0

        dist, left, right = heapq.heappop(self.midSeats)
        dist = abs(dist)

        if leftDist>=rightDist and leftDist>=dist:
            # pick first seat
            # but here.. who is the first interval???
            # hmm... I am stuck again????????
            self.firstSeatTaken = True
            heapq.heappush(self.midSeats, [
                           self.firstMidSeat//2*-1, 0, self.firstMidSeat])
            return 0
        elif rightDist>leftDist and rightDist>dist:
            self.lastSeatTaken = True
            heapq.heappush(self.midSeats, [
                           (self.cap-1-self.lastSeat)//2*-1, self.lastSeat, self.cap-1])
            return self.cap-1
        else:
            # okay.. only now I choose a mid seat
            # but then when the top seat is not valid???
            # lets say I kick invalid ranges out in leave function 
            pos = dist + left 
            self.taken[pos] = [left, right]
            heapq.heappush(self.midSeats, [(pos-left)//2*-1, left, pos])
            heapq.heappush(self.midSeats, [(right-pos)//2*-1, pos, right])
            
            if right == self.firstMidSeat:
                self.firstMidSeat = pos
            if left == self.lastMidSeat:
                self.lastMidSeat = pos
            if right != self.cap-1:
                self.taken[right][0] = pos
            if left != 0:
                self.taken[left][1] = pos

            return pos 
    

    def leave(self, p: int) -> None:

        if p == 0:
            self.firstSeatTaken = False
        elif p == self.cap-1:
            self.lastSeatTaken = False
        else:
            # we need to delete two ranges 
            # left to p , p to right
            # in a heap.. it is hard..
            pLeft, pRight = self.taken[p]
            self.taken.pop(p)
            if not self.taken:
                self.midSeats = []
                return

            seats = []
            for dist,left,right in self.midSeats:
                if left == p or right == p:
                    continue
                seats.append([dist, left, right])
            seats.append([(pRight-pLeft)//2*-1, pLeft, pRight])
            self.midSeats = seats
            heapq.heapify(self.midSeats)


            if p == self.firstMidSeat:
                self.firstMidSeat = pRight
            if p == self.lastMidSeat:
                self.lastMidSeat = pLeft

"""
okay..

one hour.. is gone
and I am still no where... 

I should admit it.. nows

and I checked other people's code.. no one really offered very concise and good solution
maybe this is trully a pratical problem..

hard to solve so many edge cases

okay.. I am beaten.. 
I'll just brute force
"""


class ExamRoom:

    def __init__(self, n: int):
        self.takenSeats = SortedList()
        self.lastSeat = n -1
        
    def seat(self) -> int:
        if not self.takenSeats:
            self.takenSeats.add(0)
            return 0
        
        leftDist = (self.takenSeats[0], 0)
        rightDist = (self.lastSeat - self.takenSeats[-1], self.lastSeat)

        maxDist = leftDist
        for s1,s2 in zip(self.takenSeats, self.takenSeats[1:]):
            dist = (s2-s1)//2
            if dist > maxDist[0]:
                maxDist = (dist, s1+dist)
        
        if rightDist[0] > maxDist[0]:
            maxDist = rightDist
        
        self.takenSeats.add(maxDist[1])
        return maxDist[1]

    def leave(self, p: int) -> None:
        self.takenSeats.remove(p)

"""
Runtime: 5027 ms, faster than 18.43% of Python3 online submissions for Exam Room.
Memory Usage: 17.3 MB, less than 76.44% of Python3 online submissions for Exam Room.
"""

if __name__ == '__main__':
    for i, arg in enumerate([[10], [], [], [], [0], [4], [], [], [], [], [], [], [], [], [], [0]]):
        if i > 0:
            print(f"before i={i}, taken: {er.takenSeats}")
        if i == 0:
            er = ExamRoom(*arg)
        elif not arg:
            print(er.seat())
        else:
            er.leave(*arg)
        if i > 0:
            print(f"after i={i}, taken: {er.takenSeats}")
            print()
