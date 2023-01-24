"""
https://leetcode.com/problems/product-of-two-run-length-encoded-arrays/?envType=study-plan&id=algorithm-iii

feel like a two pointer problem?
i -> A
j -> B

then just get the shorter length of A[i] B[j] and write buffer values
"""


from typing import List


class Solution:
    def findRLEArray(self, encoded1: List[List[int]], encoded2: List[List[int]]) -> List[List[int]]:

        i=j=0
        tmp = []
        usedFreq1 = usedFreq2 = 0
        while i<len(encoded1) and j<len(encoded2):

            val1,freq1 = encoded1[i]
            val2,freq2 = encoded2[j]

            minFreq = min(freq1-usedFreq1, freq2-usedFreq2)
            tmp.append([val1*val2, minFreq])

            if freq1-usedFreq1 == freq2-usedFreq2:
                i+=1
                j+=1
                usedFreq1 = usedFreq2 = 0
            elif freq1-usedFreq1>freq2-usedFreq2:
                usedFreq1 += minFreq
                usedFreq2 = 0
                j+=1
            else:
                usedFreq2 += minFreq
                usedFreq1 = 0
                i+=1
        
        res = []
        i=0
        while i<len(tmp):
            rle = tmp[i]
            while i+1<len(tmp) and tmp[i][0] == tmp[i+1][0]:
                rle[1] += tmp[i+1][1]
                i+=1
            res.append(rle)
            i+=1

        return res

"""
Runtime: 5795 ms, faster than 22.66% of Python3 online submissions for Product of Two Run-Length Encoded Arrays.
Memory Usage: 73.4 MB, less than 7.88% of Python3 online submissions for Product of Two Run-Length Encoded Arrays.

okay let me see if I can improve a bit
"""


if __name__ == '__main__':
    s = Solution()
    print(s.findRLEArray(encoded1=[[1, 3], [2, 3]], encoded2=[[6, 3], [3, 3]]))
    print(s.findRLEArray(
        encoded1=[[1, 3], [2, 1], [3, 2]], encoded2=[[2, 3], [3, 3]]))
    print(s.findRLEArray(encoded1=[[1, 5],[2,1], [2, 3]], encoded2=[[6, 1],[5,3],[4,2],[3, 3]]))

