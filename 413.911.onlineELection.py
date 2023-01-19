"""
https://leetcode.com/problems/online-election/

at 50-60% mental capacity I read this problem
it is probably like 

1. go thru the persons and times in constructor 
    for each person, establish the sorted set 
    search bisect_left find its own slot.. add to 1 or set to 1
2. hmm.. what wait.. it changes over time.. we need to query at/under a specific time
    so do I keep a time,winner pair?
    and previous votees can be stored in a map
    I maintain the highest votees
    it says the recent one wins if there is a tie..
    that feels like, there is a map+linkedList
    as a matter of fact I don't even need to keep the linkedlist for very long 

"""


import bisect
from collections import defaultdict
from typing import List


class TopVotedCandidate:

    def __init__(self, persons: List[int], times: List[int]):
        self.maxFreq = 0
        self.votees = defaultdict(int)
        self.maxFreqVotees = []
        self.timeAndWinner = []

        for p,t in zip(persons,times):
            self.votees[p] += 1
            if self.votees[p] > self.maxFreq:
                self.maxFreq = self.votees[p]
                self.maxFreqVotees = [p]
            elif self.votees[p] == self.maxFreq:
                self.maxFreqVotees.append(p)
            
            self.timeAndWinner.append((t, self.maxFreqVotees[-1]))
    

    def q(self, t: int) -> int:

        idx = bisect.bisect_right(self.timeAndWinner, (t,10000))
        return self.timeAndWinner[idx-1][1]

"""
Runtime: 662 ms, faster than 77.66% of Python3 online submissions for Online Election.
Memory Usage: 19.9 MB, less than 61.54% of Python3 online submissions for Online Election.

"""

if __name__ == '__main__':

    calls = ["TopVotedCandidate", "q", "q", "q", "q", "q", "q"]
    args = [[[0, 1, 1, 0, 0, 1, 0], [0, 5, 10, 15, 20, 25, 30]], [3], [12], [25], [15], [24], [8]]

    for call,arg in zip(calls, args):
        if call == 'TopVotedCandidate':
            s = TopVotedCandidate(*arg)
        else:
            print(s.q(*arg))

