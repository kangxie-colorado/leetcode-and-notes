"""
https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/


"""


from typing import List


class Solution:
    def minDays(self, bloomDay: List[int], m: int, k: int) -> int:
        # the argument is m, don't reuse the m in the sense of mid of l and r... 
        if len(bloomDay) < m*k:
            return -1

        def canMake(day):
            need = k
            bouquets = 0
            for bloom in bloomDay:
                if bloom > day:
                    need = k
                    continue
                
                need -= 1
                if need == 0:
                    bouquets += 1
                    need = k
            return bouquets>=m
            

        l,r = 1, 10**9+1
        while l<r:
            mid = l + (r-l)//2
            if canMake(mid):
                r = mid
            else:
                l = mid+1
        return l if l <10**9+1 else -1
    
if __name__ == '__main__':
    print(Solution().minDays(bloomDay = [1,10,3,10,2], m = 3, k = 1))