"""
https://leetcode.com/problems/time-based-key-value-store/?envType=study-plan&id=binary-search-ii


"""


from collections import defaultdict
from sortedcontainers import SortedList


class TimeMap:

    def __init__(self):
        self.kv = defaultdict(SortedList)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.kv[key].add((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        # 1 <= key.length, value.length <= 100
        # 'z' < 'zz' : this is true

        idx = self.kv[key].bisect_left((timestamp, "z"*101))
        if idx == 0:
            return ""
        # tricky part is I am search "z"*100... therefore.. using idx-1
        return self.kv[key][idx-1][1]

"""
Runtime: 883 ms, faster than 50.55% of Python3 online submissions for Time Based Key-Value Store.
Memory Usage: 71.7 MB, less than 52.15% of Python3 online submissions for Time Based Key-Value Store.
"""
