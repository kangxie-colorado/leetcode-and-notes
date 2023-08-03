"""
https://leetcode.com/problems/find-median-from-data-stream/


redo this
"""


import heapq


class MedianFinder:

    def __init__(self):
        self.largeHalf = []  # min heap, smallest number is used
        self.smallHalf = []  # max heap, biggest number is used

    def addNum(self, num: int) -> None:

        if not self.largeHalf or num > self.largeHalf[0]:
            heapq.heappush(self.largeHalf, num)
        else:
            heapq.heappush(self.smallHalf, -num)

        if abs(len(self.largeHalf) - len(self.smallHalf)) > 1:
            if len(self.largeHalf) > len(self.smallHalf):
                heapq.heappush(self.smallHalf, -heapq.heappop(self.largeHalf))
            else:
                heapq.heappush(self.largeHalf, -heapq.heappop(self.smallHalf))

    def findMedian(self) -> float:
        if len(self.largeHalf) > len(self.smallHalf):
            return self.largeHalf[0]
        elif len(self.largeHalf) < len(self.smallHalf):
            return -self.smallHalf[0]
        else:
            return (self.largeHalf[0] - self.smallHalf[0])/2

"""
Runtime: 561 ms, faster than 92.55% of Python3 online submissions for Find Median from Data Stream.
Memory Usage: 35.6 MB, less than 93.24% of Python3 online submissions for Find Median from Data Stream.

ah the follow up
https://leetcode.com/problems/find-median-from-data-stream/discuss/286238/Java-Simple-Code-Follow-Up

if all numbers are in [0...100], buckets and use index as the number.. 
count the frequency, accumulate frequencies to reach the n/2 or n/2+1

if 99% numbers ar ein [0..100], then <0 or >100 1%
the median must still be in 0-100..

that said, you just need to keep a count of number <0.. 
then still count the frequencies
"""

if __name__ == '__main__':
    mf = MedianFinder()
    mf.addNum(1)
    mf.addNum(2)
    print(mf.findMedian())
    mf.addNum(3)
    print(mf.findMedian())
