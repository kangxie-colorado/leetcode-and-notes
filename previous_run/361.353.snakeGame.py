"""
https://leetcode.com/problems/design-snake-game/?envType=study-plan&id=programming-skills-iii

the acceptance is so low 
be careful


"""


from collections import deque
from typing import List


class SnakeGame:
    def __init__(self, width: int, height: int, food: List[List[int]]):
        self.height = height
        self.width = width
        self.food = food[::-1]
        self.snake = deque([(0, 0)])
        self.body = {(0,0)}

    def move(self, direction: str) -> int:
        dx, dy = {'R': (0, 1), 'L': (0, -1), 'D': (1, 0),
                  'U': (-1, 0)}[direction]
        x, y = self.snake[0]
        nx, ny = x+dx, y+dy

        if nx < 0 or nx >= self.height or ny < 0 or ny >= self.width:
            return -1

        # bite self at any pos but the tail is dead
        if (nx, ny) != self.snake[-1] and (nx, ny) in self.body:
            return -1

        if self.food and [nx, ny] == self.food[-1]:
            self.food.pop()
        else:
            self.body.remove(self.snake[-1])
            self.snake.pop()
            
        self.snake.appendleft((nx, ny))
        self.body.add((nx,ny))

        return len(self.snake)-1

"""
Runtime: 259 ms, faster than 84.18% of Python3 online submissions for Design Snake Game.
Memory Usage: 15.7 MB, less than 92.24% of Python3 online submissions for Design Snake Game.

changed the body to a set
Runtime: 243 ms, faster than 94.69% of Python3 online submissions for Design Snake Game.
Memory Usage: 15.8 MB, less than 74.08% of Python3 online submissions for Design Snake Game.
"""

if __name__ == '__main__':
    for i,arg in enumerate([[3,2,[[1,2],[0,1]]],["R"],["D"],["R"],["U"],["L"],["U"]]):
        if i==0:
            snake = SnakeGame(*arg)
        else:
            print(snake.move(*arg))