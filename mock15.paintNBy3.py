"""
happen to solve it
insights.. 
1. starting 2nd row, each row is only impacted by the row above
2. colors are equal, no specifial weight 
3. there are only two colors row, or three colors row
4. how will they impact the next row

turns out 
2-color row: 
  will generate 2-colors*3, and 3-colors*2
3-color row:
  will generate 2-colors*2, and 2-colors*2

so it can be solved 
"""

class Solution:
    def numOfWays(self, n: int) -> int:
        mod = 10**9+7
        
        if n==1:
            return 12
        
        twoColors = 6
        threeColors = 6
        
        for i in range(2,n+1):
            newTwo = (twoColors*3 + threeColors*2)%mod
            newThree = (twoColors*2 + threeColors*2)%mod
            twoColors, threeColors = newTwo, newThree
            
        return (twoColors+threeColors)%mod