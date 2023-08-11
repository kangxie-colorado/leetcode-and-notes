import heapq
from typing import List


class Solution:
    def kthSmallest(self, mat: List[List[int]], k: int) -> int:
        m,n = len(mat), len(mat[0])
        firstCol = []
        pickIdx = [0] * m
        for i in range(m):
            firstCol.append(mat[i][0])
        h = []
        heapq.heappush(h, firstCol)
        while k:
            heapq.heappop(h)


""""
once again, I dive into the solution too early
... 

I thought I just need need to store the smallest array but I would need the next set of number to give me the smallest
always do case study

and yeah.. my mental state is hurting me
this is sorted by sum of sun-array.. not by the array itself

it is also asking for kth-sum. not kth-array
so it will be a bit easier?

in the heap, store [val,i,j], when chosen, pop replace the last number and enqueue the next number

1 10 10
1 4  5
2 3  6

start: [1,1,2]  heap: [3,4,10]
pop 3: (3,2,1), the sum becomes 5, heap [4,6,10]
pop 4: (4,1,1), replace 1, the sum becomes 8, heap[5,6,10]
ugh.. the next array is [1,4,2]

so I totally mis-understood the question
how important it is to understand the question thoroughly... 

maybe I store the increase of sum??
still not right

maybe I store the final sum
still not right but getting a bit closer

maybe I can use a bitmap (0-41) to represnet the array
then I got m*bitmap

for each of them, I put the next bigger number to the bitmap
or maybe not bitmap, just number 

cause this k is <200, so it will be end before n^m
lets try coding a bit
"""

class Solution:
    def kthSmallest(self, mat: List[List[int]], K: int) -> int:
        m,n = len(mat), len(mat[0])

        S = 0
        selections = [0]*m
        for i in range(m):
          S += mat[i][0]
        k=1

        h = []
        for i in range(m):
          if n>1:
            delta = mat[i][1] - mat[i][0]
            newSelctions = list(selections)
            newSelctions[i] = 1
            heapq.heappush(h, (S+delta, i,1, newSelctions))

        added = set()
        while k<K:
            k += 1
            S,x,y,sels = heapq.heappop(h)
            sels[x] = y
            for x, sY in enumerate(sels):
               if sY + 1 < n:
                  delta = mat[x][sY+1] - mat[x][sY]
                  newSels = list(sels)
                  newSels[x] = sY + 1
                  if tuple(newSels) in added:
                     continue
                  added.add(tuple(newSels))
                  heapq.heappush(h, (S+delta, x, sY+1, newSels))
            
        
        return S

"""
surprisinly, it passed
the code is not pretty

but interestingly I did this before I solved it using a merging function 
so the idea is to reduce the complexity first

thinking of merging two rows, how to do that?
could do the same as above but also could 
adding every number of rows[1] by first number of rows[2]
then using a heap.. 

we only need k number, so yeah, it is still kind of bound by k
and thinking that

the two rows don't have to be same length
but we do need to cache the intermediate result for further merges

let me try
"""

class Solution:
    def kthSmallest(self, mat: List[List[int]], K: int) -> int:
        
        def kthSmallestPairSum(A, B):
          m,n = len(A), len(B)

          h = []
          for i in range(m):
              h.append((A[i] + B[0], i,0))
          heapq.heapify(h)

          res = []
          k = K
          while h and k>0:
              val, x,y = heapq.heappop(h)
              res.append(val)
              if y+1<n:
                heapq.heappush(h, (A[x] + B[y+1], x, y+1))
              k-=1
          
          return res

        res = mat[0]
        m = len(mat)
        for i in range(1,m):
           res = kthSmallestPairSum(res, mat[i])
        
        return res[K-1]
             
          


if __name__ == '__main__':
   s = Solution()
   print(s.kthSmallest(mat = [[1,3,11],[2,4,6]], K = 9))
   print(s.kthSmallest(mat = [[1,3,11],[2,4,6]], K = 5))
   print(s.kthSmallest(mat = [[1,10,10],[1,4,5],[2,3,6]], K = 7))