"""
https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/

when the clock is ticking 
I solved it with the brute force way

brute force happens when I build the graph because I see at most 1000 nodes
so at most 1000000 edges 

it of course is O(n**2)
afterwards... check the Lee's post
https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/discuss/197668/Count-the-Number-of-Islands-O(N)

some genius ideas 

5. Unify index
Struggle between rows and cols?
You may duplicate your codes when you try to the same thing on rows and cols.
In fact, no logical difference between col index and rows index.

An easy trick is that, add 10000 to col index.
So we use 0 ~ 9999 for row index and 10000 ~ 19999 for col.


6. Search on the index, not the points
When we search on points,
we alternately change our view on a row and on a col.

We think:
a row index, connect two stones on this row
a col index, connect two stones on this col.

In another view:
A stone, connect a row index and col.       <=== exactly this!!!

Have this idea in mind, the solution can be much simpler.
The number of islands of points,
is the same as the number of islands of indexes.

7. now union find 
the union number will be the stones that can be left
how to get to that..

of course, just go thru each one and find its root... put to a set
... then you know

I actually thought about union-find... but I didn't figure out how to do 2D union find
the index trick did that for me.. 
"""


from typing import List


class Solution:
    def removeStones(self, stones: List[List[int]]) -> int:
        uf = {}

        def find(x):
            if uf[x] != x:
                uf[x] = find(uf[x])

            return uf[x]

        def union(x, y):
            # this will refresh the value each time back to x, setdefault will only do that when there is a missing value
            # uf[x] = x
            # uf[y] = y
            uf.setdefault(x, x)
            uf.setdefault(y, y)
            uf[find(x)] = find(y)

        for i, j in stones:
            union(i, j+20000)

        return len(stones) - len({find(x) for x in uf})


""""
[[0,0],[2,2],[10000,2]]

haha.. 10000 is here to trick you
0 <= xi, yi <= 10**4

okay.. let me add 20000

Runtime: 328 ms, faster than 68.77% of Python3 online submissions for Most Stones Removed with Same Row or Column.
Memory Usage: 14.7 MB, less than 78.87% of Python3 online submissions for Most Stones Removed with Same Row or Column.
"""

"""
continue to read
https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/discuss/197693/Java-Union-Find
it gives..
Runtime: 179 ms, faster than 29.69% of Java online submissions for Most Stones Removed with Same Row or Column.
Memory Usage: 54.5 MB, less than 17.01% of Java online submissions for Most Stones Removed with Same Row or Column.


this guy is O(n**2) too...
then why union-find.. just dfs/bfs.. all the same... 
"""


if __name__ == '__main__':
    s = Solution()
    print(s.removeStones([[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]))
