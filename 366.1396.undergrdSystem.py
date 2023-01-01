"""
https://leetcode.com/problems/design-underground-system/?envType=study-plan&id=programming-skills-iii


"""

from collections import defaultdict


def defaultAvgTime():
    return [0,0]

class UndergroundSystem:

    def __init__(self):
        self.customers = {} # id: check-in-stn,time; gets popped when check-out
        self.averageTime = defaultdict(defaultAvgTime) # station1, station2: [sum, trips]

    def checkIn(self, id: int, stationName: str, t: int) -> None:
        self.customers[id] = (stationName, t)

    def checkOut(self, id: int, stationName: str, t: int) -> None:
        checkInStn, checkInTime = self.customers.pop(id)
        total, trips = self.averageTime[checkInStn, stationName]
        self.averageTime[checkInStn, stationName] = [total+t-checkInTime, trips+1]

    def getAverageTime(self, startStation: str, endStation: str) -> float:
        total, trips = self.averageTime[startStation, endStation]
        return total/trips

"""
Runtime: 256 ms, faster than 82.52% of Python3 online submissions for Design Underground System.
Memory Usage: 23.9 MB, less than 88.56% of Python3 online submissions for Design Underground System.
"""