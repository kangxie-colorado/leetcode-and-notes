from typing import List


class Solution:
    def minHeightShelves(self, books: List[List[int]], shelfWidth: int) -> int:
        

        def f(idx, remain, rowHeight, runingHeight):
            if idx == len(books):
                return runingHeight+rowHeight
            
            if remain < books[idx][0]:
                # must go to next row
                return f(idx, shelfWidth, 0, runingHeight+rowHeight)
            
            if remain == shelfWidth:
                # must place to this row.. no point to go next row which is non-sense
                return f(idx+1, remain-books[idx][0],  max(rowHeight, books[idx][1]), runingHeight)

            # place in this row or next row
            return min ( 
                f(idx+1, remain-books[idx][0],  max(rowHeight, books[idx][1]), runingHeight), # this row
                f(idx, shelfWidth, 0, rowHeight+runingHeight) # place to next row
            )
            

        return f(0,shelfWidth,0,0)
    
class Solution:
    def minHeightShelves(self, books: List[List[int]], shelfWidth: int) -> int:
        

        def f(idx, remain, rowHeight, runingHeight):
            if idx == len(books):
                return runingHeight+rowHeight
            
            if remain < books[idx][0]:
                # must go to next row
                return f(idx, shelfWidth, 0, runingHeight+rowHeight)
            
            if remain == shelfWidth or books[idx][1]<rowHeight:
                # must place to this row.. no point to go next row which is non-sense
                return f(idx+1, remain-books[idx][0],  max(rowHeight, books[idx][1]), runingHeight)

            # place in this row or next row
            return min ( 
                f(idx+1, remain-books[idx][0],  max(rowHeight, books[idx][1]), runingHeight), # this row
                f(idx, shelfWidth, 0, rowHeight+runingHeight) # place to next row
            )
            

        return f(0,shelfWidth,0,0)

class Solution:
    def minHeightShelves(self, books: List[List[int]], shelfWidth: int) -> int:
        cache = {}

        def f(idx, remain, rowHeight, runingHeight):
            if idx == len(books):
                return runingHeight+rowHeight
            
            if (idx,remain) in cache:
                return cache[(idx,remain)]
            
            res = 0
            if remain < books[idx][0]:
                # must go to next row
                res = f(idx, shelfWidth, 0, runingHeight+rowHeight)
            
            elif remain == shelfWidth or books[idx][1]<rowHeight:
                # must place to this row.. no point to go next row which is non-sense
                res = f(idx+1, remain-books[idx][0],  max(rowHeight, books[idx][1]), runingHeight)
            else:
            # place in this row or next row
                res = min ( 
                    f(idx+1, remain-books[idx][0],  max(rowHeight, books[idx][1]), runingHeight), # this row
                    f(idx, shelfWidth, 0, rowHeight+runingHeight) # place to next row
                )
            cache[(idx,remain)] = res
            return res
            

        return f(0,shelfWidth,0,0)
  
if __name__ == '__main__':
    s = Solution()
    print(s.minHeightShelves( books = [[1,1],[2,3],[2,3],[1,1],[1,1],[1,1],[1,2]], shelfWidth = 4))
    print(s.minHeightShelves( books = [[1,3],[2,4],[3,2]], shelfWidth = 6))