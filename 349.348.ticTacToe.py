"""
https://leetcode.com/problems/design-tic-tac-toe/


"""


from collections import defaultdict


class TicTacToe:

    def __init__(self, n: int):
        self.rowSets = [defaultdict(int) for _ in range(n)]
        self.colSets = [defaultdict(int) for _ in range(n)]
        self.diag = defaultdict(int)  # x==y
        self.revDiag = defaultdict(int) # x+y = n-1
        self.n = n

    def move(self, row: int, col: int, player: int) -> int:
        self.rowSets[row][player] += 1
        self.colSets[col][player] += 1
        if row==col: 
            self.diag[player] += 1
        if row+col == self.n-1:
            self.revDiag[player] += 1

        if self.n in [self.rowSets[row][player], self.colSets[col][player], self.diag[player],  self.revDiag[player]]:
            return player
        
        return 0

"""
Runtime: 92 ms, faster than 88.64% of Python3 online submissions for Design Tic-Tac-Toe.
Memory Usage: 16.7 MB, less than 85.98% of Python3 online submissions for Design Tic-Tac-Toe.
"""