"""
https://leetcode.com/problems/design-log-storage-system/?envType=study-plan&id=programming-skills-iii

I think this is a natrual trie structure 
and by experiment, the granularity means compares up to that level 

and it is inclusive both ends

writing a bit code.. I think maybe we don't need to use try
use hashmap?

1, "2017:01:01:23:59:59"
will be like

yearMap[2017].add(1)
monthMap[01],add(1)
...
secMap[01].add(1)

then I just run the intersection...
seems like not very smart but why don't I try

okay... had a try but soon realized that won't pass logically easily 
"""

from collections import defaultdict
from typing import List

from sortedcontainers import SortedList


class LogSystem_Tried_HashMaps_But_Not_Gonna_Work:

    def __init__(self):
        # self.years = defaultdict(set)
        # self.months = defaultdict(set)
        # self.days = defaultdict(set)
        # self.hours = defaultdict(set)
        # self.minutes = defaultdict(set)
        # self.seconds = defaultdict(set)
        self.granularities = ["Year", "Month", "Day", "Hour", "Minute", "Second"]

        self.logs = [defaultdict(set) for _ in range(6)]


    def put(self, id: int, timestamp: str) -> None:
        # year,month,day,hour,minute,second = timestamp.split(':')

        # self.years[year].add(id)
        # self.months[month].add(id)
        # self.days[day].add(id)
        # self.hours[hour].add(id)
        # self.minutes[minute].add(id)
        # self.seconds[second].add(id)
        for idx,key in enumerate(timestamp.split(':')):
            self.logs[idx][int(key)].add(id)

    def retrieve(self, start: str, end: str, granularity: str) -> List[int]:
        res = set()
        granIdx = self.granularities.index(granularity)

        for i, (s, e) in enumerate(zip(start.split(':'), end).split(':')):
            if i > self.granularities.index(granularity):
                break

            s,e = int(s), int(e)
            if not res:
                res = set(self.logs[i][s])
            for j in range(s,e+1):
                res = res.intersection(self.logs[i][j])
        
        return list(set)


# Your LogSystem object will be instantiated and called as such:
# obj = LogSystem()
# obj.put(id,timestamp)
# param_2 = obj.retrieve(start,end,granularity)


class LogSystem:

    def __init__(self):
        self.granularities = ["Year", "Month", "Day", "Hour", "Minute", "Second"]

        self.logs = SortedList()

    def put(self, id: int, timestamp: str) -> None:
        self.logs.add((*[int(f) for f in timestamp.split(':')], id))

    def retrieve(self, start: str, end: str, granularity: str) -> List[int]:
        granIdx = self.granularities.index(granularity)
        startFields = [int(f) for f in start.split(':')]
        endFields = [int(f) for f in end.split(':')]

        fieldsMax = [10000, 12,31,23,59,59]
        i =  5
        
        while i>granIdx:
            startFields[i] = fieldsMax[i]
            endFields[i] = fieldsMax[i] 
            i-=1

        while startFields[i] == 0:
            i-=1
        startFields[i] -= 1

        left = self.logs.bisect_right((*startFields, 0))
        right = self.logs.bisect_right((*endFields, 500))

        return [f[6] for f in self.logs[left:right]]

"""
Runtime: 71 ms, faster than 71.43% of Python3 online submissions for Design Log Storage System.
Memory Usage: 14.6 MB, less than 22.45% of Python3 online submissions for Design Log Storage System.

as I guessed, the edge case around 31/30/28-th day didn't really matter

ah.. okay.. this is even concise
https://leetcode.com/problems/design-log-storage-system/discuss/105016/Python-Straightforward-with-Explanation

and no need to sort
"""



        # Your LogSystem object will be instantiated and called as such:
        # obj = LogSystem()
        # obj.put(id,timestamp)
        # param_2 = obj.retrieve(start,end,granularity)


class LogSystem:

    def __init__(self):
        self.logs = []

    def put(self, id: int, timestamp: str) -> None:
        self.logs.append((id, timestamp))

    def retrieve(self, s: str, e: str, granularity: str) -> List[int]:
        index = {'Year': 5, 'Month': 8, 'Day': 11,
                 'Hour': 14, 'Minute': 17, 'Second': 20}[granularity]
        start = s[:index]
        end = e[:index]

        return [id for id, ts in self.logs if start<=ts[:index]<=end]

"""
Runtime: 43 ms, faster than 97.96% of Python3 online submissions for Design Log Storage System.
Memory Usage: 14.2 MB, less than 67.35% of Python3 online submissions for Design Log Storage System.

"""


if __name__ == '__main__':
    ls = LogSystem()
    ls.put(1, "2017:01:01:23:59:59")
    ls.put(2, "2017:01:01:22:59:59")
    ls.put(3, "2016:01:01:00:00:00")
    print(ls.retrieve("2016:01:01:01:01:01", "2017:01:01:23:00:00", "Year"))
    print(ls.retrieve("2016:01:01:01:01:01", "2017:01:01:23:00:00", "Hour"))

