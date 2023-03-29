"""
https://leetcode.com/problems/cat-and-mouse/


a super hard!
I cannot figure out on my own for sure - so I watched other's solution 
    bfs and from the end status trace back

    the idea is to color the graph
    color-0: draw.. 
    color-1: mouse wins
    color-2: cat wins

    we paint the graph using three states: m, c, t
            mouse pos, cat pos, whose turn

    pre-known colored areas:
        [0,*,*]: when mouse has reached hole 0.. mouse wins
        [i,i,*]: when cat lands on the same cell as mouse.. cat wins

    we expand these areas to whole graph as much as possible
        enqueue those known colored areas and trace back (on the time horizon)
            then check the status of status[m,c,t]
            if it is t==1, mouse's turn and at this point cat will win... 
                then that means from last move, cat will catch on mouse
                i.e. cat will move from a neighboring cell to [m,c,t]
                and cat must make that move.. 
                therefore 
                    those cells will be colored as cat wins
                    those cells will be enqueued 

            if it is t==2, cat's turn and at this point mouse will win...
                then that means from last move, mouse will go into hole 0 (actually the winning position, not necessarily hole-0 yet)
                i.e. mouse will move from neighboring cell to [m,c,t]
                and mouse must make that move.. 
                therefore 
                    those cells will be colored as mouse win
                    those cells will be enqueued
            
            for other cases
                mouse's turn and at this point mouse will win..
                    then last move was cat's and because moving to here mouse will win.. so cat will not play this move
                    thus skip that cell
                same goes for cat's turn and cat will win
            
                BUT...
                if at last move, all "its" next move(including current move) will lead to opposite's win then there is no chance last mover can win
                in this case, that cell's destination is also decided to be current mover's win

        
        of course.. when that status has been visited.. we don't want to create cycle
        and cat cannot move into hole 0...
        
    after all expoloration, if mouse/cat are on some un-painted area (colro-0), draw

really complext..
let me do it...

"""


from collections import deque
from collections import defaultdict, deque


class Solution(object):
    def catMouseGame(self, graph):
        N = len(graph)

        # mouse,cat,turn
        # turn-1: mouse's turn
        # turn-2: cat's turn
        # value-1: mouse wins
        # value-2: cat wins
        # value-0: draw
        color = defaultdict(int)
        q = deque()
        for i in range(N):
            color[0,i,1] = color[0,i,2] = 1
            q.append((0, i, 1))
            q.append((0, i, 2))
            if i>0:

                color[i,i,1] = color[i,i,2] = 2
                q.append((i, i, 1))
                q.append((i, i, 2))
        
        def neighborMoves(m,c,t):
            if t==1:
                # current move is mouse then we look for cat
                # next/last move is cat
                for c_move in graph[c]:
                    if c_move and c: # no hole-0 for cat
                        yield m,c_move,3-t 
            else:
                # current move is cat then we look for mouse
                for m_move in graph[m]:
                    yield m_move, c, 3-t
        
        def allOpposeWin(m2,c2,t2):
            if t2==1:
                # mouse move.. check if any next cat move leads to cat win
                # if not.. then I can bail
                for m_move in graph[m2]:
                    if color[m_move,c2,2] != 2:
                        return False
            else:
                # cat move.. check if any next mouse move leads to mouse win
                # if not.. then I can bail
                for c_move in graph[c2]:
                    if c_move and color[m2,c_move,1] != 1:
                        return False
            return True

        

        visited = set()
        while q:
            m,c,t = q.popleft()

            if (m,c,t) in visited:
                continue
            visited.add((m,c,t))

            for m2,c2,t2 in neighborMoves(m,c,t):
                if t2 == color[m,c,t]:
                    # t2: cat, and current cell is cat win
                    # t2: mouse, and current cell is mouse win
                    # this is a shortened from
                    # assgin that last cell to the corresponding color
                    color[m2, c2, t2] = color[m, c, t]
                    q.append((m2, c2, t2))
                else:
                    # current mover is standing at a cell where it will win
                    # then last mover don't want to move to here.. if possible
                    # but there is scenario that it has not choice but to surrender
                    # if they are in such states... 
                    # that scenarios is if and only if all next moves of last move lead to current mover's win
                    # ugh.. to say it is confusing enough
                    # bail = False
                    # for m3, c3, t3 in neighborMoves(m2,c2,3-t2):
                    #     # if color[m3,c3,t3] != t:
                    #     if color[m3, c3, 3-t3] != 3-t2:

                    #         # if there is one possible skip then bail
                    #         # the skip is color not opposite's win.. can be my win or draw
                    #         bail = True
                    #         break 
                    # if not bail:
                    if allOpposeWin(m2,c2,t2):
                        color[m2, c2, t2] = 3-t2
                        q.append((m2, c2, t2))
        return color[1,2,1]


class Solution(object):
    def catMouseGame(self, graph):
        """
        :type graph: List[List[int]]
        :rtype: int
        """
        # arr = [[[0]*2 for j in range(55)] for i in range(55)]
        color = defaultdict(int)
        q = deque()
        for i in range(1, len(graph)):
            # arr[i][i][0], arr[i][i][1] = 2, 2
            # arr[i][0][0], arr[i][0][1] = 1, 1

            color[i, i, 1] = color[i, i, 2] = 2
            color[0, i, 1] = color[0, i, 2] = 1

            q.append((0, i,1))
            q.append((0, i,2))
            q.append((i, i, 1))
            q.append((i, i, 2))
        while q:
            m,c,turn = q.popleft()
            s = color[m,c,turn]
            if turn == 2:
                # cat's move; find previous move of mouse
                for pre_move in graph[m]:
                    if color[pre_move, c, 1] != 0:
                        continue
                    if s == 1:
                        color[pre_move, c, 1] = 1
                        q.append((pre_move, c,  1))
                    elif s == 2:
                        cat_win = True
                        for nex_move in graph[pre_move]:
                            # if arr[c][nex_move][0] != 2:
                            if color[nex_move,c,2] != 2:
                                cat_win = False
                                break
                        if cat_win:
                            # arr[c][pre_move][1] = 2
                            color[pre_move,c,1] = 2
                            q.append((pre_move, c,  1))
            else:
                for pre_move in graph[c]:
                    # if arr[pre_move][m][0] != 0:
                    if color[m,pre_move,2] != 0:
                        continue
                    if pre_move != 0:
                        if s == 2:
                            # arr[pre_move][m][0] = 2
                            color[m,pre_move,2] = 2
                            q.append((m, pre_move, 2))
                        elif s == 1:
                            mouse_win = True
                            for nex_move in graph[pre_move]:
                                if nex_move != 0:
                                    # if arr[nex_move][m][1] != 1:
                                    if color[m,nex_move,1] != 1:
                                        mouse_win = False
                                        break
                            if mouse_win:
                                # arr[pre_move][m][0] = 1
                                color[m,pre_move,2] = 1
                                q.append((m, pre_move, 2))
        return color[1,2,1]

""""
SUPER HARD...
I feel overwhelmed.. even after I learned
leave this to a futuer time...

okay.. it was that visited control in the way
and this works

"""


class Solution(object):
    def catMouseGame(self, graph):
        N = len(graph)

        # mouse,cat,turn
        # turn-1: mouse's turn
        # turn-2: cat's turn
        # value-1: mouse wins
        # value-2: cat wins
        # value-0: draw
        color = defaultdict(int)
        q = deque()
        for i in range(1,N):
            color[0, i, 1] = color[0, i, 2] = 1
            q.append((0, i, 1))
            q.append((0, i, 2))
            color[i, i, 1] = color[i, i, 2] = 2
            q.append((i, i, 1))
            q.append((i, i, 2))

        def neighborMoves(m, c, t):
            if t == 1:
                # current move is mouse then we look for cat
                for c_move in graph[c]:
                    if c_move:  # no hole-0 for cat
                        yield m, c_move, 3-t
            else:
                # current move is cat then we look for mouse
                for m_move in graph[m]:
                    yield m_move, c, 3-t

        while q:
            m, c, t = q.popleft()
            if (m,c,t) == (1,2,1):
                return color[1,2,1]

            for m2, c2, t2 in neighborMoves(m, c, t):
                if color[m2, c2, t2] != 0:
                    continue
                if t2 == color[m, c, t]:
                    # t2: cat, and current cell is cat win
                    # t2: mouse, and current cell is mouse win
                    # this is a shortened from
                    # assgin that last cell to the corresponding color
                    color[m2, c2, t2] = color[m, c, t]
                    if (m2,c2,t2) == (1,2,1):
                        return color[m2, c2, t2]
                    q.append((m2, c2, t2))
                else:
                    # current mover is standing at a cell where it will win
                    # then last mover don't want to move to here.. if possible
                    # but there is scenario that it has not choice but to surrender
                    # if they are in such states...
                    # that scenarios is if and only if all next moves of last move lead to current mover's win
                    # ugh.. to say it is confusing enough
                    bail = False
                    for m3, c3, t3 in neighborMoves(m2, c2, t):
                        if color[m3, c3, 3-t3] != 3-t2:
                            # if there is one possible skip then bail
                            # the skip is color not opposite's win.. can be my win or draw
                            bail = True
                            break
                    if not bail:
                        color[m2, c2, t2] = t
                        if (m2,c2,t2) == (1,2,1):
                            return color[m2, c2, t2]
                        q.append((m2, c2, t2))
        return color[1, 2, 1]


"""
Runtime: 1178 ms, faster than 19.51% of Python3 online submissions for Cat and Mouse.
Memory Usage: 14.7 MB, less than 79.27% of Python3 online submissions for Cat and Mouse.
"""
if __name__ == '__main__':
    s = Solution()
    print(s.catMouseGame([[2, 3], [3, 4], [0, 4], [0, 1], [1, 2]]))
    print(s.catMouseGame(graph = [[2,5],[3],[0,4,5],[1,4,5],[2,3],[0,2,3]]))