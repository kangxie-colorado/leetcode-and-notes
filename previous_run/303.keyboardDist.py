from collections import defaultdict
import heapq


class Solution:
    def minimumDistance(self, word: str) -> int:
        # brute force using heap
        def dist(coord1, coord2):
            x1, y1 = coord1
            x2, y2 = coord2
            return abs(x1-x2) + abs(y1-y2)

        coords = []
        counter = defaultdict(int)
        for c in word:
            diff = ord(c) - ord('A')
            coords.append((diff//6, diff % 6))
            counter[(diff//6, diff % 6)] += 1

        res = 10**9

        for i in range(len(coords)):
            for j in range(i+1, len(coords)):
                copy = counter.copy()
                h1 = []
                h2 = []

                for k in range(i+1, len(coords)):
                    if k == j:
                        continue
                    heapq.heappush(
                        h1, (dist(coords[i], coords[k]), coords[k][0], coords[k][1]))

                for k in range(j+1, len(coords)):
                    heapq.heappush(
                        h2, (dist(coords[j], coords[k]), coords[k][0], coords[k][1]))

                run = 0
                while h1 and h2:
                    d1, _, _ = h1[0]
                    d2, _, _ = h2[0]

                    if d1 < d2:
                        d, x, y = heapq.heappop(h1)
                    else:
                        d, x, y = heapq.heappop(h2)
                    if copy[(x, y)] > 0:
                        run += d
                        copy[(x, y)] -= 1

                h = h1 or h2
                while h:
                    d, x, y = heapq.heappop(h)
                    if copy[(x, y)] > 0:
                        run += d
                        copy[(x, y)] -= 1

                res = min(res, run)

        return res


if __name__ == '__main__':
    s = Solution()

    print(s.minimumDistance("TUGR"))
