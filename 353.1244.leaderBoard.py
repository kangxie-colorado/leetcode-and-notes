"""
https://leetcode.com/problems/design-a-leaderboard/
"""


from collections import defaultdict

from sortedcontainers import SortedList


from sortedcontainers import SortedList


class Leaderboard:

    def __init__(self):
        self.players = defaultdict(int)
        self.scores = SortedList()

    def addScore(self, playerId: int, score: int) -> None:
        oldScore = self.players[playerId]
        newScore = oldScore + score
        self.players[playerId] = newScore
        if oldScore:
            self.scores.remove(oldScore)

        self.scores.add(newScore)

    def top(self, K: int) -> int:
        return sum(self.scores[-K:])

    def reset(self, playerId: int) -> None:
        if self.players[playerId]:
            self.scores.remove(self.players[playerId])
        self.scores.add(0)
        self.players[playerId] = 0

"""
Runtime: 52 ms, faster than 98.77% of Python3 online submissions for Design A Leaderboard.
Memory Usage: 14.9 MB, less than 11.11% of Python3 online submissions for Design A Leaderboard.
"""