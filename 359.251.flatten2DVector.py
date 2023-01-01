"""
https://leetcode.com/problems/flatten-2d-vector/?envType=study-plan&id=programming-skills-iii

I jumped into thinking a recursive solution
and even build a tree with a back pointer to parent...

but luckily I did take a look at the hints
the title asks 2D vector

why don't I treat it like a 2D array???
row and col

but nah.. it can nest more than once.. 
however then in itself.. it is a 2D array

wait


Implement the Vector2D class:

Vector2D(int[][] vec) initializes the object with the 2D vector vec.

it should be a 2D array for sure.. 

okay.. 

["Vector2D", "next", "next", "next", "hasNext", "hasNext", "next", "hasNext"]
[[[[1, 2], [3], [4]]], [], [], [], [], [], [], []]

I was misled by this example
two nested [[]] should be treated as air

check this
Vector2D vector2D = new Vector2D([[1, 2], [3], [4]]);

"""


from typing import List


class Vector2D:

    def __init__(self, vec: List[List[int]]):
        self.vec = vec
        self.x = 0
        self.y = 0
        # shi ke jing ji yue jie shi da shi
        while self.x < len(self.vec) and not len(self.vec[self.x]):
            self.x += 1

    def next(self) -> int:
        val = self.vec[self.x][self.y]
        self.y += 1
        while self.x < len(self.vec) and self.y == len(self.vec[self.x]):
            self.y = 0
            self.x += 1
        return val

    def hasNext(self) -> bool:
        return self.x < len(self.vec)


"""
Runtime: 87 ms, faster than 79.75% of Python3 online submissions for Flatten 2D Vector.
Memory Usage: 19.3 MB, less than 51.07% of Python3 online submissions for Flatten 2D Vector.

ah... I was stuggling with the the responsibilities between next and hasNext
cause I think in iterator, it would actually call hasNext() before next()

but maybe here.. next() can call hasNext() to make the code a lit more organized
"""


class Vector2D:

    def __init__(self, vec: List[List[int]]):
        self.vec = vec
        self.x = 0
        self.y = 0

    def next(self) -> int:
        if self.hasNext():
            val = self.vec[self.x][self.y]
            self.y += 1
            return val

    def hasNext(self) -> bool:
        while self.x < len(self.vec) and self.y == len(self.vec[self.x]):
            self.y = 0
            self.x += 1
        return self.x < len(self.vec)

"""
Runtime: 88 ms, faster than 78.83% of Python3 online submissions for Flatten 2D Vector.
Memory Usage: 19.3 MB, less than 51.07% of Python3 online submissions for Flatten 2D Vector.

actually this is still not so good
it says next() is always valid.. so testing hasNext() is duplicated

maybe define a moveToNext()
"""


class Vector2D:

    def __init__(self, vec: List[List[int]]):
        self.vec = vec
        self.x = 0
        self.y = 0

    def _ignoreInvalid(self):
        while self.x < len(self.vec) and self.y == len(self.vec[self.x]):
            self.y = 0
            self.x += 1

    def next(self) -> int:
        self._ignoreInvalid()
        val = self.vec[self.x][self.y]
        self.y += 1
        return val

    def hasNext(self) -> bool:
        self._ignoreInvalid()
        return self.x < len(self.vec)
