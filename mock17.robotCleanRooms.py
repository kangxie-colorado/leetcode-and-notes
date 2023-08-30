# """
# This is the robot's control interface.
# You should not implement it, or speculate about its implementation
# """
from collections import deque


class Robot:
   def move(self):
       """
       Returns true if the cell in front is open and robot moves into the cell.
       Returns false if the cell in front is blocked and robot stays in the current cell.
       :rtype bool
       """

   def turnLeft(self):
       """
       Robot will stay in the same cell after calling turnLeft/turnRight.
       Each turn will be 90 degrees.
       :rtype void
       """

   def turnRight(self):
       """
       Robot will stay in the same cell after calling turnLeft/turnRight.
       Each turn will be 90 degrees.
       :rtype void
       """

   def clean(self):
       """
       Clean the current cell.
       :rtype void
       """

class Solution:
    def cleanRoom(self, robot):
        """
        :type robot: Robot
        :rtype: None
        """
        UP,RIGHT,DOWN,LEFT = 0,1,2,3
        def backOff(facing):
            robot.turnLeft()
            robot.turnLeft()
            robot.move()
            return (facing+2)%4

        def detect(dir, facing):
            if facing == dir:
                open = robot.move()
                if open:
                  facing = backOff(dir)
            elif (facing+1)%4 == dir: # turn right
                robot.turnRight()
                facing = dir
                open = robot.move()
                if open:
                  facing = backOff(dir)
            elif (facing+2)%4 == dir: # turn back
                robot.turnLeft()
                robot.turnLeft()
                facing = dir
                open = robot.move()
                if open:
                  facing = backOff(dir)
            else: # turn left
                robot.turnLeft()
                facing = dir
                open = robot.move()
                if open:
                  facing = backOff(dir)
            
            return open,facing
        
        # move to open cells
        def move(dir, facing):
            if facing == dir:
                robot.move()
            elif (facing+1)%4 == dir: # turn right
                robot.turnRight()
                facing = dir
                robot.move()
            elif (facing+2)%4 == dir: # turn back
                robot.turnLeft()
                robot.turnLeft()
                facing = dir
                robot.move()
            else: # turn left
                robot.turnLeft()
                facing = dir
                robot.move()
                
            return facing

        def detectNeighbor(x,y, nx,ny, facing):
            if x==nx:
                if ny == y-1:
                    # detect left
                    open,facing = detect(LEFT, facing)
                    
                if ny == y+1:
                    # detect right
                    open,facing = detect(RIGHT, facing)
            else:
                if nx == x-1:
                    # detect UP
                    open, facing = detect(UP, facing)
                
                if nx == x+1:
                    # detect down
                    open, facing = detect(DOWN, facing)
            return open, facing
                    

        empty = set()
        wall = set()
        cleaned = set()
        stack = []
        stack.append((0,0,UP,0,0))
        empty.add((0,0))

        def findPath(x1,y1,x2,y2):
            parent = {}
            visited = set()
            stack = [(x1,y1)]
            while stack:
                x,y = stack.pop()
                if (x,y) in visited:
                    continue
                visited.add(x,y)
                if (x,y) == (x2,y2):
                    break
                for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                  nx,ny = x+dx,y+dy
                  if (nx,ny) in cleaned:
                      stack.append((nx,ny))
                      parent[(nx,ny)] = (x,y)
            
            path = []
            x,y = x2,y2
            while (x,y) != (x1,y1):
                path.append((x,y))
                (x,y) = parent[(x,y)]
            
            path.reverse()
            return path


        def moveToNei(oldx, oldy, x,y, facing):
          if oldx == x:
              if y == oldy-1: # move left
                  facing = move(LEFT, facing)
              else: # move right
                  facing = move(RIGHT, facing)
          else:
              if x == oldx-1: # move up
                  facing = move(UP, facing)
              else: # move down
                  facing = move(DOWN, facing)

        def moveTo(oldx, oldy, x,y, facing):
            if oldx==x and oldy==y:
                return facing
            
            # move to adjacent cells
            if (oldx==x and abs(oldy-y)==1) or (oldy==y and abs(oldx-x)==1):
                moveToNei(oldx,oldy, x, y, facing)
            
            # else I need find a path in cleaned path
            path = findPath(oldx, oldy, x, y)
            for nextX, nextY in path:
                facing = moveToNei(oldx, oldy, nextX, nextY)
                oldx, oldy = nextX, nextY

            return facing

        while stack:
            x,y,facing,oldx,oldy = stack.pop()
            if (x,y) in cleaned:
                continue
            facing = moveTo(oldx,oldy,x,y,facing)
            robot.clean()
            cleaned.add((x,y))

            for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx,ny = x+dx,y+dy
                if (nx,ny) in wall:
                    continue
                
                open,facing = detectNeighbor(x,y,nx,ny,facing)
                if open:
                    stack.append((nx,ny,facing,x,y))
                    empty.add((nx,ny))
                else:
                    wall.add((nx,ny))


"""
needless to say, this is too complicted
and remember there is a sentence

I think this is too complicated, is there any simpler way? ask the interviewer...
so yeah.. I messed up with this

that dfs+backtrack is actually not super complicated and I gave it a thought but didn't dive into that..
I was too stubbon to work on the idea I had

now let me do that
"""


class Solution:
    def cleanRoom(self, robot):
        visited = set()
        # up, right, down, left (0,1,2,3)
        dirs = [(-1,0), (0,1), (1,0), (0,-1) ]

        def clean(x,y, facing):
            robot.clean()
            visited.add((x,y))
            # at the level, I visit my 4 neighbors if I can
            # I turn right 4 times... to face 4 neighbors and move
            # if hit wall, I will not clean that cell and turn right to next one
            for i in range(4):
                nx,ny = x+dirs[(facing+i)%4][0], y+dirs[(facing+i)%4][1]
                
                if (nx,ny) not in visited and robot.move():
                    clean(nx, ny, (facing+i)%4)
                
                robot.turnRight()
            
            # I backtrack and maintain the facing
            robot.turnRight()
            robot.turnRight()
            robot.move()
            robot.turnRight()
            robot.turnRight()
        
        clean(0,0,0)
            


