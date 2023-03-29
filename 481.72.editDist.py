"""
https://leetcode.com/problems/edit-distance/?envType=study-plan&id=dynamic-programming-iii

it looks pretty hard - but ac ratio is pretty high as well..
guess it is a decisio tree fan out

f(i,j): represents from i-th in word1 and j-th in word2, how many steps are needed
    it will be 
    min (
        insert, f(i,j+1) + 1
        delete, f(i+1,j) + 1
        replace, f(i+1,j+1) + 1
        or when word1[1]==word2[2], f(i+1,j+1) <-- actually this could be the optmize way.. so this goes its own way
    )

    base will be 
        c1==c2, return 0
        c1!=c2 and one is "", return 1 (or actually this will generalize to base case naturally)

could give a try
"""


from functools import cache


class Solution:
    def minDistance(self, word1: str, word2: str) -> int:

        @cache
        def edit(i,j):
            if i==len(word1) or j==len(word2):
                return len(word1)-i + len(word2)-j
            
            if word1[i] == word2[j]:
                return edit(i+1,j+1)
            
            return min(
                edit(i,j+1),
                edit(i+1,j),
                edit(i+1,j+1)
            ) + 1
        
        return edit(0,0)

"""
Runtime: 101 ms, faster than 90.49% of Python3 online submissions for Edit Distance.
Memory Usage: 17 MB, less than 74.08% of Python3 online submissions for Edit Distance.
"""

if __name__ == '__main__':
    s = Solution()
    print(s.minDistance(word1="horse", word2="ros"))
    print(s.minDistance(word1="intention", word2="execution"))
    print(s.minDistance("dinitrophenylhydrazine", "acetylphenylhydrazine"))
