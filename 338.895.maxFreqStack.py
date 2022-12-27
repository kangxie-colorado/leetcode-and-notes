"""
https://leetcode.com/problems/maximum-frequency-stack/?envType=study-plan&id=programming-skills-iii


I think I did this before in two ways.. 
let me try to do it again
"""

"""
1. use a map to store num to freq 
2. use a stack to store the number? (freq, index, number) 

this will use a lot of memory 
"""


from collections import defaultdict
import heapq


class FreqStack:

    def __init__(self):
        self.numsFreqs = defaultdict(int)
        self.numsHeap = []
        self.seq = 0

    def push(self, val: int) -> None:
        self.numsFreqs[val] += 1
        self.seq += 1
        heapq.heappush(self.numsHeap, (-self.numsFreqs[val], -self.seq, val))

    def pop(self) -> int:
        
        _,_,val = heapq.heappop(self.numsHeap)
        self.numsFreqs[val] -= 1

"""
Runtime: 414 ms, faster than 72.54% of Python3 online submissions for Maximum Frequency Stack.
Memory Usage: 22.7 MB, less than 64.48% of Python3 online submissions for Maximum Frequency Stack.

only 38 test cases.. not able to tell the memory 
now another way.. the map stores a stack on this frequencies

and move between map-buckets while the frequency changes
actually no need to move around, just append the same number to higher freq list..
then remove.. because there are multiple number instances that reflects different frequencies 
"""


class FreqStack:

    def __init__(self):
        # store the list in the order of being added in the corresponding frequency bucket
        self.freqs = defaultdict(list)
        # store each number's frequency
        self.nums = defaultdict(int)
        self.maxFreq = 0
        

    def push(self, val: int) -> None:
        self.nums[val] += 1
        self.freqs[self.nums[val]].append(val)
        self.maxFreq = max(self.maxFreq, self.nums[val])

    def pop(self) -> int:
        val = self.freqs[self.maxFreq].pop()
        self.nums[val] -= 1
        while self.maxFreq and  len(self.freqs[self.maxFreq])==0:
            self.maxFreq -= 1
        
        return val

"""
Runtime: 353 ms, faster than 88.26% of Python3 online submissions for Maximum Frequency Stack.
Memory Usage: 22.4 MB, less than 94.52% of Python3 online submissions for Maximum Frequency Stack.

so in fact, the memory worry I had for my first solution was not warranted.
it grows with number but shrinks with pops 

the problem might be the seq.. 
"""